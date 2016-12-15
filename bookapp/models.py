from .boilerplate import Model

from sqlalchemy import Column, Integer, String, ForeignKey


class Book(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    author_id = Column(Integer, ForeignKey('author.id'))


class Author(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
