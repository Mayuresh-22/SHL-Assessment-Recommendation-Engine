from typing import List
from bs4 import BeautifulSoup
from langchain_core.documents import Document
from app.pydantic_models.data_model import IndividualTest
from app.services.scraper.base_scraper import BaseScraper
from app.utils.envs import Envs


class CatalogueScraper(BaseScraper):
    """
    This class scraps the assessment catalogue from the SHL website.
    """
    
    def extract_individual_tests(self, url: str) -> List[IndividualTest]:
        soup = BeautifulSoup(self.crawl(url), "html.parser")
        # Page contains two tables, Pre-packaged Job Solutions and Individual Test
        # we want to extract links from the Individual Test table only
        # Skip the first 14 rows which are headers and assessment rows of 
        # Pre-packaged Job Solutions table
        
        _table_rows = []
        if "start=0" in url:
            _table_rows = soup.find_all("tr")[14:]
        else: 
            _table_rows = soup.find_all("tr")[1:]
        _individual_tests = []
        
        for row in _table_rows:
            cols = row.find_all("td")
            test_link =Envs.BASE_SHL_URL + cols[0].a["href"]  # type: ignore
            test_name = cols[0].a.string  # type: ignore
            remote_support = "Yes" if cols[1].span else "No"  # type: ignore
            adaptive_support = "Yes" if cols[2].span else "No"  # type: ignore
            test_type = [
                ttype.string for ttype in cols[3].find_all("span")
            ]
            
            _individual_tests.append(IndividualTest(
                page_content="",  # type: ignore
                url=test_link,  # type: ignore
                name=test_name,  # type: ignore
                remote_support=remote_support,  # type: ignore
                adaptive_support=adaptive_support,  # type: ignore
                description="",
                duration=0,
                test_type=test_type  # type: ignore
            ))
        
        return _individual_tests


if __name__ == "__main__":
    print(CatalogueScraper().extract_individual_tests("https://www.shl.com/products/product-catalog/?start=0&type=1&type=1"))
