import datetime
import json


def custom_dumps(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return str(obj)
    else:
        json.dumps(obj, default=custom_dumps)
