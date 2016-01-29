'''
Daniel Kronovet
dbk2123@columbia.edu

Code to set up the PostgreSQL database

psql commands reference:

\l - list databases
\c <db name> - connect to db
\dt - list tables in current db
'''

import sqlalchemy
from sqlalchemy import Table, Column, MetaData, Sequence
from sqlalchemy import BigInteger, Integer, Unicode, DateTime
from sqlalchemy.exc import DataError

from config import db_uri

engine = sqlalchemy.create_engine(db_uri, echo=False)

metadata = MetaData(engine)

tweets = Table('tweets', metadata,
   Column('id', Integer, Sequence('tweet_id_seq'), primary_key=True),
   Column('tweet_id', BigInteger),
   Column('user_id', BigInteger),
   Column('user_location', Unicode(128)),
   Column('created_at', DateTime(timezone=True)),
   Column('text', Unicode(560)), # 140 * 4 bytes (max unicode)
)

if __name__ == '__main__':
    import sys
    action = sys.argv[1]

    if action == 'create':
        print 'Creating tables...'
        metadata.create_all()
    elif action == 'drop':
        print 'Dropping tables...'
        metadata.drop_all()