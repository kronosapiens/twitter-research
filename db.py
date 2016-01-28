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

from config import db

engine = sqlalchemy.create_engine(db, echo=False)

metadata = MetaData(engine)

tweets = Table('tweets', metadata,
   Column('id', Integer, Sequence('tweet_id_seq'), primary_key=True),
   Column('tweet_id', BigInteger),
   Column('user_id', BigInteger),
   Column('user_location', Unicode(128)),
   Column('created_at', DateTime(timezone=True)),
   Column('text', Unicode(560)), # 140 * 4 bytes (max unicode)
)

metadata.create_all()
# metadata.drop_all()