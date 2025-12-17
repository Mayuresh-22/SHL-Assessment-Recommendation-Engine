from importlib import metadata
from typing import List
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStore
from langchain_text_splitters import TextSplitter

from app.pydantic_models.data_model import IndividualTest
from app.services.scraper.assessment_scraper import AssessmentScraper
from app.services.scraper.catalogue_scraper import CatalogueScraper
from app.services.text_splitter.factory import get_text_splitter
from app.services.vector_store.factory import get_vector_store


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
    ) -> None:
        self.catalogue_scraper = catalogue_scraper
        self.assessment_scraper = assessment_scraper
        self.vector_store = vector_store
        self.text_splitter = text_splitter
    
    def create_documents(self, tests: List[IndividualTest]) -> List[Document]:
        all_docs: List[Document] = []
        for test in tests:
            all_docs.append(
                Document(
                    page_content=test.page_content,
                    metadata={
                        "url": test.url,
                        "name": test.name,
                        "adaptive_support": test.adaptive_support,
                        "duration": test.duration,
                        "remote_support": test.remote_support,
                        "test_type": test.test_type                       
                    }
                )
            )
        return all_docs
        
    
    def ingest_data(self):
        all_tests = []
        
        for page in range(0, 373, 12):
            url = f"https://www.shl.com/products/product-catalog/?start={page}&type=1"
            all_tests = self.catalogue_scraper.extract_individual_tests(url)
            self.assessment_scraper.extract_assessment_details(all_tests)
        
        all_docs = self.create_documents(all_tests)

        split_docs = self.text_splitter.split_documents(all_docs)
        
        self.vector_store.add_documents(split_docs)
        print(f"Ingested {len(split_docs)} documents into the vector store.")
        
        return len(split_docs)
    
    def clear_data(self):
        """Clears all data from the vector store."""
        self.vector_store.delete(delete_ALL=True)
        print("Cleared all data from the vector store.")