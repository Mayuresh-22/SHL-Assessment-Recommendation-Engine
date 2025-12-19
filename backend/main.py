import json
from pprint import pprint

from app.services.balancer.balancer import ResultBalancer
from app.services.ingester.data_ingester import DataIngester
from app.services.llm.factory import get_llm
from app.services.query.query_transformer import QueryTransformer
from app.services.recommender.recommender import Recommender
from app.services.reranker.factory import get_reranker
from app.services.retriever.factory import get_retriever
from app.services.scraper.assessment_scraper import AssessmentScraper
from app.services.scraper.catalogue_scraper import CatalogueScraper
from app.services.text_splitter.factory import get_text_splitter
from app.services.vector_store.factory import get_vector_store
from app.utils.envs import Envs
from app.utils.config import load_config


def run_ingestion(config: dict):
    """Run the data ingestion pipeline"""
    catalogue_scraper = CatalogueScraper()
    assessment_scraper = AssessmentScraper()
    vector_store = get_vector_store()
    text_splitter = get_text_splitter()
    
    ingester = DataIngester(
        catalogue_scraper=catalogue_scraper,
        assessment_scraper=assessment_scraper,
        vector_store=vector_store,
        text_splitter=text_splitter,
        start_from_batch=config.get("DATA_INGESTION_START_FROM_BATCH", 0),
        end_at=config.get("DATA_INGESTION_END_AT", 372),
        start_fresh=config.get("DATA_INGESTION_START_FRESH", False),
        total_batches=config.get("DATA_INGESTION_TOTAL_BATCHES", 31),
        batch_size=config.get("DATA_INGESTION_BATCH_SIZE", 12)
    )
    
    ingester.ingest_data()
    print("Data ingestion completed successfully!")


def main():
    config = load_config()
    
    # Run data ingestion only if the flag is enabled
    if config.get("DATA_INGESTION", False):
        print("Starting data ingestion...")
        run_ingestion(config)
        print("Completed data ingestion.")
    else:
        print("Data ingestion is disabled. Skipping...")
    

if __name__ == "__main__":
    main()
