"""List of regexes used by the crawlers."""

import re


RE_LINK = re.compile(r'(?:((?:http[s]?:\/\/)?(?:www|www2)?(?:[0-9-a-z]+\.[a-z\/\.?=&]*))|(?:href="(.*?)"))')
RE_EMAIL = re.compile(r'([\w\.,]+@[\w\.,]+\.\w+)')
