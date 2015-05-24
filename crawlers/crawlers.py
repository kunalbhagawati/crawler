"""Holds the classes that implement the crawlers."""

import requests
import re
import urllib
from pprint import pprint
import time
import sys

from crawler.utils.jsonhelpers import EnhancedJSONEncoder


reEmail = re.compile(r'([\w\.,]+@[\w\.,]+\.\w+)')

reLink = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
# reLink = re.compile(r'href="(.*?)"')


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
        return EnhancedJSONEncoder().encode(self.result)

    def crawl(self, url, maxlevel=3, max_links=None, **kwargs):
        """Entry to crawling function.
        Resets the crawled links."""

        # clear the crawled set and the result
        self.crawled = set()
        if hasattr(self, 'result'):
            del self.result
        return self._crawl_wrapper(url, maxlevel, max_links, **kwargs)

    def _crawl_wrapper(self, url, maxlevel=3, max_links=None, **kwargs):
        """Wrapper function for the crawling function.
        This can be overwritten by the child class for its own formatting.
        """

        # should not do a recursive crawl for the same link
        if url in self.crawled:
            return {
                    "crawl_status": False,
                    "reason": "RECURSIVE_LOOP",
                }
        self.crawled.add(url)
        time1 = time.time()
        res = self._crawl_implementation(url, maxlevel, max_links, **kwargs)
        time2 = time.time()
        res['stats'] = {'time': (time2-time1)*1000}
        self.result = res
        return res

    def _crawl_implementation(self, url, maxlevel, max_links, **kwargs):
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
        # for links upto max_links, crawl recursivly
        for link in links:
            # Get the absolute URL
            link = urllib.parse.urljoin(url, link)
            retDict['links'][link] = self._crawl_wrapper(
                    link, maxlevel-1, **kwargs)

        return retDict


# class EmailCrawler(BaseCrawler):


if __name__ == '__main__':
    url = sys.argv[1:2][0]
    pprint(BaseCrawler().crawl(url, 2))
