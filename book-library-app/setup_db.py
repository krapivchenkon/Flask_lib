# all the imports
from __future__ import with_statement
from contextlib import closing
import sqlite3

# configuration
DATABASE = 'db/library.db'
DUMP = 'lib_dump.sql'

# initializing db from script
def init_db():
	with closing(connect_db()) as db:
		with open(DUMP) as f:
			db.cursor().executescript(f.read())
			db.commit()

def connect_db(): 
	return sqlite3.connect(DATABASE)

if __name__ == '__main__':
	init_db()	

