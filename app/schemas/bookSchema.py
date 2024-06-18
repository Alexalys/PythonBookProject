# Pydantic model for request payload
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, constr, model_validator, root_validator


class BookCreate(BaseModel):
    title: str = Field(
        "", description="Title of the book", example="Great expectations"
    )
    author: Optional[str] = Field(
        None, description="Author of the book", example="Charles Dickens"
    )

    @model_validator(mode="before")
    @classmethod
    def check_title(cls, values: dict):
        title: str = values.get("title", "")
        if not title.strip():
            raise ValueError("Title must not be empty")
        return values

    def __repr__(self):
        return f"BookCreate(title={self.title!r}, author={self.author!r})"


class Book(BaseModel):
    id: int = Field(1, description="Title of the book", example="Great Expectations")
    title: str = Field(
        "", description="Title of the book", example="Great Expectations"
    )
    author: str = Field("", description="Author of the book", example="Charles Dickens")
    publicationDate: date = Field("", description="Publication date of the book")
    description: str = Field("", description="Description of the book")
    genre: str = Field("", description="Genre of the book")

    class Config:
        orm_mode = True
