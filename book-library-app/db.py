# -*- coding: utf-8 -*- 
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

'''
sqlite:///:memory: (or, sqlite://)
sqlite:///relative/path/to/file.db
sqlite:////absolute/path/to/file.db
'''
engine = create_engine('sqlite:///db/library.db')
db_session = scoped_session(sessionmaker(autocommit=False,autoflush=False,bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
	Base.metadata.create_all(bind=engine)

def get_or_create(model, **kwargs):
	object = db_session.query(model).filter_by(**kwargs).first()
	if object: 
		# basically check the obj from the db, this syntax might be wrong
		return object
	else:
		object = model(**kwargs)
		# do it here if you want to save the obj to the db
		return object

def exists(model, **kwargs):
	object = db_session.query(model).filter_by(**kwargs).first()
	if object: 
		# basically check the obj from the db, this syntax might be wrong
		return object
	else:
		return False


