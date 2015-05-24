"""Holds the classes that implement the crawlers."""

import requests
import re
import urllib
from pprint import pprint
import time
import sys
import json


reEmail = re.compile(r'([\w\.,]+@[\w\.,]+\.\w+)')

reLink = re.compile(r'href="(.*?)"')


class BaseCrawler:
    """Base crawler class."""

    def __init__(self, **kwargs):
        debug = kwargs.get('debug', False)
        self.debug = debug
        self.crawled = set()

    def check_multiprocess(self, **kwargs):
        """Checks if multithreading support is active."""

        # dummy for now.
        return False

    def as_json(self):
        """Returns the crawled result as json."""

        if not hasattr(self, 'result'):
            raise Exception("You have not crawled anything yet!")
        return json.dumps(self.result)

    def crawl(self, url, maxlevel, **kwargs):
        """Wrapper function for the crawling function."""

        # should not do a recursive crawl for the same link
        if url in self.crawled:
            return {
                    "crawl_status": False,
                    "reason": "RECURSIVE_LOOP",
                }
        self.crawled.add(url)
        time1 = time.time()
        res = self._crawl(url, maxlevel, **kwargs)
        time2 = time.time()
        res['stats'] = {'time': (time2-time1)*1000}
        self.result = res
        return res

    def _crawl(self, url, maxlevel, **kwargs):
        """Implements the crawling part."""

        if maxlevel <= 0:
            return {
                "crawl_status": False,
                "reason": "MAX_DEPTH_REACHED",
            }

        # Get the webpage
        res = requests.get(url)

        # Return if not successfull
        if (res.status_code//100) != 2:
            return {
                "crawl_status": False,
                "reason": "RESPONSE_FAIL",
                "response_status": res.status_code,
                "response_error": res.reason,
            }

        retDict = {
            'content': res,
            'links': {},
            "response_status": res.status_code,
        }
        # Find and follow all the links
        links = reLink.findall(res.text)
        for link in links:
            # Get the absolute URL
            link = urllib.parse.urljoin(url, link)
            retDict['links'][link] = self.crawl(link, maxlevel-1, **kwargs)

        return retDict

if __name__ == '__main__':
    url = sys.argv[1:2][0]
    pprint(BaseCrawler().crawl(url, 2))
