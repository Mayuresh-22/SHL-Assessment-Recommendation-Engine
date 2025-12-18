from modulefinder import test
from typing import List, Optional
from bs4 import BeautifulSoup
from langchain_core.documents import Document
import tqdm

from app.pydantic_models.data_model import IndividualTest
from app.services.scraper.base_scraper import BaseScraper

TEST_TYPE_MAP = {
    "A": "Ability & Aptitude",
    "B": "Biodata & Situational Judgement",
    "C": "Competencies",
    "D": "Development & 360",
    "E": "Assessment Exercises",
    "K": "Knowledge & Skills",
    "P": "Personality & Behavior",
    "S": "Simulations"
}

class AssessmentScraper(BaseScraper):
    """
    This class is responsible for scraping assessment details from its respective pages.
    """
    
    def extract_assessment_details(
        self, 
        tests: List[IndividualTest], 
        container_class_selector: str = "col-12 col-md-8",
        container_row_selector: str = "product-catalogue-training-calendar__row typ",
    ):
        for test in tqdm.tqdm(tests, unit=("assessments")):
            soup = BeautifulSoup(self.crawl(test.url), "html.parser")
            
            container = soup.find("div", {"class": container_class_selector}).find_all(  # type: ignore
                "div", attrs={"class": container_row_selector}
            )  # type: ignore

            description = container[0].p.text  # type: ignore
            
            # Additional details for relevant recommendation
            job_levels = None
            if len(container) > 2:
                job_levels = container[1].p.text  # type: ignore
                
            languages = None
            if len(container) > 3:
                languages = container[2].p.text  # type: ignore
            
            duration = 0
            if container[-1].p:
                duration_text = container[-1].p.text  # type: ignore
                extracted_duration = ''.join(filter(str.isdigit, duration_text))
                if extracted_duration.isdigit():
                    duration = int(extracted_duration)
                else:
                    duration = 0
            
            test.description = description  # type: ignore
            test.duration = duration
            test.page_content = f"""
Assessment name: {test.name}

Description: {description}

{self.handle_job_levels(job_levels)}
{self.handle_testing_lang(languages)}

{self.handle_duration(duration)}
{self.handle_remote_testing(test.remote_support == "Yes")}

Test category: {self.handle_test_types(test.test_type)}.
"""
            print(f"Test {test.name}, desc: {description}, duration: {duration}, job_levels: {job_levels}, languages: {languages}\n")

    def handle_job_levels(self, job_levels: Optional[str]) -> str:
        if job_levels is None:
            return ""
        return f"This assessment is designed for {job_levels} roles."
    
    def handle_remote_testing(self, remote_support: bool) -> str:
        return f"This assessment {'supports' if remote_support else 'does not support'} remote testing."
    
    def handle_testing_lang(self, languages: Optional[str]) -> str:
        if languages is None:
            return ""
        return f"It supports testing in {languages}."

    def handle_test_types(self, test_types: List[str]) -> str:
        descriptions = [TEST_TYPE_MAP.get(ttype, "Unknown") for ttype in test_types]
        return ", ".join(descriptions)
    
    def handle_duration(self, duration: int) -> str:
        bucket = ""
        if duration <= 30:
            bucket = "short"
        elif 30 < duration <= 60:
            bucket = "medium"
        else:
            bucket = "long"
        return f"This is a {bucket}-duration assessment."
            
