"""Mixins that help validate the kind of links the crawler has to crawl."""

import urllib


class BasicValidator:
    """Only returns a set from the list of links provided."""

    def get_valid_links(self, links):
        """Returns the set of links that are valid.
        Dummy function, meant to be extended by the child class.

        Must return a single valued iterable.
        """

        return set([x for y in links for x in y if self._validate(x)])

    def _validate(self, link):
        return True


class URLOnlyValidator(BasicValidator):
    """Does not permit crawling of text files, documents, etc.
    i.e. only crawls links."""

    ALLOWED_TYPES = {
        'html',
        'aspx',
        'php',
        'htm',
    }

    def _validate(self, link):
        return (True
                if (urllib
                    .parse
                    .urlparse(link)[2]
                    .split('/')[-1]
                    .split(".")[-1])
                in self.ALLOWED_TYPES else False)
