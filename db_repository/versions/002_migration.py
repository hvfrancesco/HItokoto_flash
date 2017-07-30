from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
storia = Table('storia', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('titolo', String(length=64)),
    Column('body', String(length=10000)),
    Column('timestamp', DateTime),
    Column('auth_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['storia'].columns['titolo'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['storia'].columns['titolo'].drop()
