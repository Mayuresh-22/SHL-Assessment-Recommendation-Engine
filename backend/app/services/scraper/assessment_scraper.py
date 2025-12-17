from typing import List
from bs4 import BeautifulSoup
from langchain_core.documents import Document

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
    
    def extract_assessment_details(self, tests: List[IndividualTest], class_selector: str = "col-12 col-md-8"):
        assessment_details = []
        for test in tests:
            soup = BeautifulSoup(self.crawl(test.url), "html.parser")
            container = soup.find("div", {"class": class_selector}).find_all(  # type: ignore
                "div", attrs={"class": "product-catalogue-training-calendar__row typ"}
            )  # type: ignore
            
            description = container[0].p.string  # type: ignore
            
            # Additional details for relevant recommendation
            job_levels = container[1].p.string.split(", ")  # type: ignore
            languages = container[2].p.string  # type: ignore
            
            duration = 0
            if len(container) == 4:
                duration_text = container[3].p.text  # type: ignore
                duration = int(''.join(filter(str.isdigit, duration_text)))
            
            test.description = description  # type: ignore
            test.duration = duration
            
            test.page_content = f"""
Assessment name: {test.name}

Description: {description}

This assessment is designed for {", ".join(job_levels)} roles.
It supports testing in {languages}.

This is a {self.duration_bucketing(duration)}-duration assessment and {"supports" if test.remote_support == "Yes" else "does not support"} remote testing.

Test category: {self.test_type_description(test.test_type)}.
"""

    def test_type_description(self, test_types: List[str]) -> str:
        descriptions = [TEST_TYPE_MAP.get(ttype, "Unknown") for ttype in test_types]
        return ", ".join(descriptions)
    
    def duration_bucketing(self, duration: int) -> str:
        if duration == 0:
            return "not specified"
        if duration <= 30:
            return "short"
        elif 30 < duration <= 60:
            return "medium"
        else:
            return "long"
            
