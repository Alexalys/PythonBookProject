from datetime import datetime
import re
from fastapi.encoders import jsonable_encoder
from openai import OpenAI
import json

from app.configuration.errors import LlmError
from app.models.Book import BookModel
from app.schemas.bookSchema import BookCreateSchema
from app.utils.LoggerProvider import logger


class LlmProvider:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LlmProvider, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "client"):
            self.client = OpenAI()

    def generate_book_info(self, book: BookCreateSchema) -> BookModel:
        logger.info("Generating book info")
        info = json.dumps(jsonable_encoder(book, exclude_none=True), indent=2)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. The response should be a list of JSON objects with the following fields: title:str, author:str, description:str, genre:str, publication_date: Date.",
                },
                {
                    "role": "user",
                    "content": f"Generate a list of JSONs with information for the book {info}.",
                },
            ],
        )
        modified_content = re.sub(
            r"```json\n?|```", "", response.choices[0].message.content
        )
        content = json.loads(modified_content)
        if isinstance(content, list) and len(content) > 1:
            error: LlmError = LlmError()
            error.message = "multiple books found"
            error.http_code = 500
            raise error
        content[0]["publication_date"] = datetime.strptime(
            content[0]["publication_date"], "%Y-%m-%d"
        ).date()
        return BookModel(**content[0])

    def generate_reccomendations(self, books: list[BookModel]) -> list[BookModel]:
        logger.info("Generating book reccomendation")
        info = json.dumps(jsonable_encoder(books, exclude_none=True), indent=2)
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Provide JSON format as follows, along with the definition of each field:{'books': [{'title':'...', 'author':'...', 'description':'...', 'genre':'...', 'publication_date':'2020-08-04'}]} ",
                },
                {
                    "role": "user",
                    "content": f"Generate a list of JSONs with book reccomendations for reading based on the books already read. Here is an info: {info}. Books should be unique and not read before",
                },
            ],
        )
        modified_content = re.sub(
            r"```json\n?|```", "", response.choices[0].message.content
        )
        content = json.loads(modified_content)
        for item in content.get("books"):
            if "publication_date" in item:
                item["publication_date"] = datetime.strptime(
                    item["publication_date"], "%Y-%m-%d"
                ).date()

        return [BookModel(**book) for book in content.get("books")]


llm_provider: LlmProvider = LlmProvider()
