# -*- coding: utf-8 -*-
from sqlalchemy import Column, Integer, String, Sequence, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from db import Base

books_authors = Table('books_authors', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id')),
    Column('author_id', Integer, ForeignKey('authors.id'))
)

class Book(Base):
	__tablename__ = 'books'
	__plural__ = 'Books'
	__url__ = 'book'
	id = Column(Integer, primary_key=True)
	name = Column(String(50))
	description = Column(String())
	authors = relationship("Author",secondary=books_authors, backref="books")

	def __init__(self, name, description):
		self.name = name
		self.description = description 

	def __repr__(self):
		return "%s" % self.name

class Author(Base):
	__tablename__ = 'authors'
	__plural__ = 'Authors'
	__url__ = 'author'
	id = Column(Integer, primary_key=True)
	name = Column(String(50))

	def __init__(self, name):
		self.name = name

	def __repr__(self):
		return "%s" % (self.name)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(50))
    fullname = Column(String(50))
    password = Column(String(12))

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
	    return "<User('%s','%s', '%s')>" % (self.name, self.fullname, self.password)

class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, Sequence('entry_id_seq'), primary_key=True)
    title = Column(String(50))
    text = Column(String(50))

    def __init__(self, title, text):
        self.title = title
        self.text = text

    def __repr__(self):
	    return "<User('%s','%s')>" % (self.title, self.text)

