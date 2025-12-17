import requests

from app.utils.envs import Envs


class BaseScraper:

    def crawl(self, url: str) -> str:
        html = requests.get(url, headers={"User-Agent": Envs.SCRAPER_USER_AGENT}).text
        return html
