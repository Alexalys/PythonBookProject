from datetime import datetime
from openai import OpenAI
import json

from app.models.Book import BookModel
from app.schemas.bookSchema import BookCreate


class LlmProvider:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LlmProvider, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "client"):
            self.client = OpenAI()

    def generate_book_info(self, book: BookCreate) -> BookModel:
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant. Provide your response in JSON format with the following fields: title:str, author:str, description:str, genre:str, publicationDate: Date.",
                },
                {
                    "role": "user",
                    "content": f"Generate information for the book {repr(book)}",
                },
            ],
        )
        content = json.loads(response.choices[0].message.content)
        content["publicationDate"] = datetime.strptime(
            content["publicationDate"], "%Y-%m-%d"
        ).date()
        return BookModel(**content)


llm_provider: LlmProvider = LlmProvider()
