from sqlalchemy import Column, Integer, String, Date
from app.models.Base import Base


class BookModel(Base):
    __tablename__ = "books"

    title = Column(String, index=True)
    author = Column(String, nullable=True)
    publicationDate = Column(Date, nullable=True)
    description = Column(String, nullable=True)
    genre = Column(String, nullable=True)
