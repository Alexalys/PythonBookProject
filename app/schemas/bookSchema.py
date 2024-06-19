# Pydantic model for request payload
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, model_validator


class BookCreateSchema(BaseModel):
    title: str = Field(
        ..., description="Title of the book", example="Great Expectations"
    )
    author: Optional[str] = Field(
        None, description="Author of the book", example="Charles Dickens"
    )
    publication_date: Optional[str] = Field(
        None, description="Publication date of the book", example="1949-06-08"
    )
    description: Optional[str] = Field(
        None,
        description="Description of the book",
        example="This novel describes some ancient times",
    )
    genre: Optional[str] = Field(
        None, description="Genre of the book", example="A dystopian novel"
    )

    @model_validator(mode="before")
    @classmethod
    def check_title(cls, values: dict):
        title: str = values.get("title", "")
        if not title.strip():
            raise ValueError("Title must not be empty")
        return values


class BookSchema(BaseModel):
    uuid: str = Field(
        ..., description="uuid", example="123e4567-e89b-12d3-a456-426614174000"
    )
    title: str = Field(
        ..., description="Title of the book", example="Great Expectations"
    )
    author: str = Field(
        ..., description="Author of the book", example="Charles Dickens"
    )
    publication_date: date = Field(
        ..., description="Publication date of the book", example="1949-06-08"
    )
    description: str = Field(
        ..., description="Description of the book", example="Some description"
    )
    genre: str = Field(
        ..., description="Genre of the book", example="A dystopian novel"
    )

    class Config:
        from_attributes = True


class BookRecommendation(BaseModel):
    title: str = Field(
        ..., description="Title of the book", example="Great Expectations"
    )
    author: str = Field(
        ..., description="Author of the book", example="Charles Dickens"
    )
    publication_date: date = Field(
        ..., description="Publication date of the book", example="1949-06-08"
    )
    description: str = Field(
        ..., description="Description of the book", example="Some description"
    )
    genre: str = Field(
        ..., description="Genre of the book", example="A dystopian novel"
    )

    class Config:
        from_attributes = True
