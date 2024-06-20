from sqlalchemy import Column, String, Date, UniqueConstraint
from app.models.Base import Base


class BookModel(Base):
    __tablename__ = "books"

    title = Column(String, index=True)
    author = Column(String, nullable=True)
    publication_date = Column(Date, nullable=True)
    description = Column(String, nullable=True)
    genre = Column(String, nullable=True)
    __table_args__ = (UniqueConstraint("title", "author", name="_title_author_uc"),)
