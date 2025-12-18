from importlib import metadata
from typing import List
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import TextSplitter
import tqdm

from app.pydantic_models.data_model import IndividualTest
from app.services.scraper.assessment_scraper import AssessmentScraper
from app.services.scraper.catalogue_scraper import CatalogueScraper
from app.services.text_splitter.factory import get_text_splitter
from app.services.vector_store.factory import get_vector_store
from app.utils.config import write_config
from app.utils.envs import Envs


class DataIngester:
    """
    This class is responsible for ingesting SHL assessment data by utilizing the
    CatalogueScraper and AssessmentScraper services.
    """
    
    def __init__(
        self, 
        catalogue_scraper: CatalogueScraper, 
        assessment_scraper: AssessmentScraper,
        vector_store: VectorStore,
        text_splitter: TextSplitter,
        start_from_batch: int = 0,
        # Actually it can be 373, cause last page only has 5 tests
        # and last page is 32nd starts from 31*12=372
        # so any number between 373-383 (inclusive) will work the same
        end_at: int = 377,
        start_fresh: bool = False,
        batch_size: int = 12,
        total_batches: int = 32
    ) -> None:
        self.catalogue_scraper = catalogue_scraper
        self.assessment_scraper = assessment_scraper
        self.vector_store = vector_store
        self.text_splitter = text_splitter
        self.start_from_batch = start_from_batch
        self.end_at = end_at
        self.start_fresh = start_fresh
        self.batch_size = batch_size
        self.total_batches = total_batches
    
    def _create_documents(self, tests: List[IndividualTest]) -> List[Document]:
        all_docs: List[Document] = []
        for test in tests:
            all_docs.append(
                Document(
                    page_content=test.page_content,
                    metadata={
                        "url": test.url,
                        "name": test.name,
                        "description": test.description,
                        "adaptive_support": test.adaptive_support,
                        "duration": test.duration,
                        "remote_support": test.remote_support,
                        "test_type": test.test_type                       
                    }
                )
            )
        return all_docs
        
    
    def ingest_data(self):
        """
        This method orchestrates the data ingestion process by scraping assessment data,
        splitting the text, and storing it in the vector store in batches.
        
        Supports resuming from specific batch in case of error/interruption.
        """
        curr_batch = self.start_from_batch
        
        loop_start = self.start_from_batch * self.batch_size
        loop_end = self.end_at
        
        try:
            for page in tqdm.tqdm(range(loop_start, loop_end, self.batch_size), unit=("catalogue pages")):
                url = Envs.SHL_PRODUCT_CATALOGUE_URL.format(page=page)
                
                tests = self.catalogue_scraper.extract_individual_tests(url)
                self.assessment_scraper.extract_assessment_details(tests)
                docs = self._create_documents(tests)
                
                split_docs = self.text_splitter.split_documents(docs)
                self.vector_store.add_documents(split_docs)
                
                curr_batch += 1
                
                # Save progress in config.json
                write_config({
                    "DATA_INGESTION_START_FROM_BATCH": curr_batch,
                    "DATA_INGESTION_END_AT": self.end_at
                })
            
            print("Data ingestion completed.")
        except Exception as e:
            print(f"Data ingestion interrupted at batch {curr_batch}, page {curr_batch+1}. Error: {e}")
            # Save progress in config.json
            write_config({
                "DATA_INGESTION_START_FROM_BATCH": curr_batch,
                "DATA_INGESTION_END_AT": self.end_at
            })
            raise e
    
    def clear_data(self):
        """Clears all data from the vector store."""
        self.vector_store.delete(delete_ALL=True)
        print("Cleared all data from the vector store.")
