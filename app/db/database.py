from typing import Iterator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session
from app.models.Base import Base
from contextlib import contextmanager


_engine = None
_session_local = None


def init_db(db_url):
    global Base, _engine, _session_local

    _engine = create_engine(db_url, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=_engine)
    _session_local = sessionmaker(autocommit=False, autoflush=False, bind=_engine)


@contextmanager
def get_session() -> Iterator[Session]:
    global _session_local
    if _session_local is None:
        raise Exception("DB is not initialized")
    db = _session_local()
    try:
        yield db
    finally:
        db.close()
