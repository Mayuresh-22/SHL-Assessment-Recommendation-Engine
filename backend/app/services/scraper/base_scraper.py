import random
import time

import requests
from fp.fp import FreeProxy

from app.utils.envs import Envs


class BaseScraper:
    
    DEFAULT_HEADERS = {
        "User-Agent": Envs.SCRAPER_USER_AGENT,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }

    def crawl(self, url: str, delay: bool = True) -> str:
        """
        Crawl a URL with browser-like headers to avoid getting blocked.
        
        Args:
            url: The URL to crawl
            delay: Whether to add a random delay before the request (default: True)
        """
        if delay:
            time.sleep(random.uniform(0.5, 0.9))
        
        session = requests.Session()
        response = session.get(url, headers=self.DEFAULT_HEADERS, timeout=30)
        response.raise_for_status()
        
        return response.text
