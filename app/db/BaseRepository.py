from sqlalchemy.orm import Session
from abc import ABC, abstractmethod


class BaseRepository(ABC):

    @abstractmethod
    def create(self, item):
        pass

    @abstractmethod
    def find_one(self, book_id: int):
        pass

    @abstractmethod
    def find_all(self, offset: int = 0, limit: int = 10):
        pass

    @abstractmethod
    def delete_one(self, book_id: int) -> int:
        pass
