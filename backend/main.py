import sys

from app.utils.config import load_config


def run_ingestion(config: dict):
    """Run the data ingestion pipeline"""
    from app.services.ingester.data_ingester import DataIngester
    from app.services.scraper.assessment_scraper import AssessmentScraper
    from app.services.scraper.catalogue_scraper import CatalogueScraper
    from app.services.text_splitter.factory import get_text_splitter
    from app.services.vector_store.factory import get_vector_store

    catalogue_scraper = CatalogueScraper()
    assessment_scraper = AssessmentScraper()
    vector_store = get_vector_store()
    
    if config.get("DATA_INGESTION_WITH_SPLIT", False):
        print("Using text splitter for data ingestion...")
        text_splitter = get_text_splitter()
    else:
        print("Not using text splitter for data ingestion...")
        text_splitter = None
    
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
    cmd_args = sys.argv[1:]
    
    # Run data ingestion only if the flag is enabled
    if config.get("DATA_INGESTION", False):
        print("Starting data ingestion...")
        run_ingestion(config)
        print("Completed data ingestion.")
    else:
        print("Data ingestion is disabled. Skipping...")
    
    if cmd_args and cmd_args[0] == "eval":
        print("Eval mode")
        # evaluate retriever and reranker
        from app.evaluation.evaluator import Evaluator
        from app.services.balancer.balancer import ResultBalancer
        from app.services.llm.factory import get_llm
        from app.services.query.query_transformer import QueryTransformer
        from app.services.retriever.factory import get_retriever
        from app.services.reranker.factory import get_reranker
        
        evaluator = Evaluator(
            retriever=get_retriever(),
            reranker=get_reranker(),
            balancer=ResultBalancer(),
            query_transformer=QueryTransformer(llm=get_llm()),
            dataset_file="app/evaluation/dataset.xlsx"
        )
        evaluator.evaluate_all()
    elif cmd_args and cmd_args[0] == "testset":
        print("Testset mode")
        # generate test set recommendations
        from app.evaluation.test_set_recommendation import TestSetRecommendation
        from app.services.balancer.balancer import ResultBalancer
        from app.services.llm.factory import get_llm
        from app.services.query.query_transformer import QueryTransformer
        from app.services.retriever.factory import get_retriever
        from app.services.reranker.factory import get_reranker

        test_set_recommender = TestSetRecommendation(
            retriever=get_retriever(),
            reranker=get_reranker(),
            balancer=ResultBalancer(),
            query_transformer=QueryTransformer(llm=get_llm()),
            dataset_file="app/evaluation/dataset.xlsx",
            results_file="test_set_predictions.csv"
        )
        test_set_recommender.run()
    else:
        print("Serve mode")
        # start the fastapi server
        import uvicorn
        from app.services.api.main import app
        
        uvicorn.run(app, host="0.0.0.0", port=8000)
    

if __name__ == "__main__":
    main()
