"""Mixins that help validate the kind of links the crawler has to crawl."""


class BasicValidator:
    """Only returns a set from the list of links provided."""

    def _get_valid_links(self, links):
        """Returns the set of links that are valid.
        Dummy function, meant to be extended by the child class.

        Must return a single valued iterable.
        """

        return set([x for y in links for x in y if x])
