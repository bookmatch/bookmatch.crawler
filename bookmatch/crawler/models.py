# -*- coding: utf-8 -*-

import sqlalchemy as sql
import sqlalchemy as sa
from sqlalchemy import Column
from sqlalchemy.orm import scoped_session, sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base

__all__ = ['DBSession', 'Content']

Base = declarative_base()
DBSession = scoped_session(sessionmaker())


class Content(Base):
    __tablename__ = 'content'

    query = DBSession.query_property()

    id = Column(sa.Integer, primary_key=True)
    isbn = Column(sa.String(16), nullable=False)
    title = Column(sa.UnicodeText(), nullable=False, default=u"")
    author = Column(sa.UnicodeText(), nullable=False, default=u"")
    # body = Column(sa.UnicodeText(), nullable=False, default=u"")
    source = Column(sa.String(16), nullable=False)
    publish_date = Column(sa.Date)
    update_at = Column(sa.DateTime)
