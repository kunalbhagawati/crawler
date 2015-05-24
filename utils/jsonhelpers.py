"""Utils for handling json."""

import json
import datetime
from requests.models import Response


class EnhancedJSONEncoder(json.JSONEncoder):
    """Extends the default JSON Encoder to handle the datetime values,
    response objects and other stuff.

    Note: For now the datetime format is hardcoded.
    This can be easily changed later.
    """

    def default(self, obj):
        if isinstance(obj, Response):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif isinstance(obj, datetime.timedelta):
            return ((datetime.datetime.min + obj)
                    .time()
                    .strftime("%Y-%m-%d %H:%M:%S"))
        else:
            return super().default(obj)
