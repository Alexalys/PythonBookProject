from sqlalchemy.orm import Session
from abc import ABC, abstractmethod


class BaseRepository(ABC):

    @abstractmethod
    def create(self, db: Session, item):
        pass

    @abstractmethod
    def find_one(self, db: Session, book_id: int):
        pass

    @abstractmethod
    def find_all(self, db: Session, offset: int = 0, limit: int = 10):
        pass
