import flask
import json

from schemainspect import get_inspector
from sqlalchemy.ext.declarative import declarative_base
from sqlbag import Base

Model = declarative_base(cls=Base)


def selectables(s):
    i = get_inspector(s)
    names = [_.name for _ in (i.selectables.values())]
    return names


class Response(flask.Response):
    @property
    def json(self):
            return json.loads(self.get_data(as_text=True))
