from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from app.db.database import Base


class BookModel(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    author = Column(String, nullable=True)
    publicationDate = Column(Date, nullable=True)
    description = Column(String, nullable=True)
    genre = Column(String, nullable=True)
