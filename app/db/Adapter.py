from app.models.Book import BookModel
from app.schemas.bookSchema import BookRecommendation


class BookAdapter:

    def to_data_source(self, book: BookModel) -> BookRecommendation:
        """
        Mapper from BookModel to BookRecommendation
        """
        return BookRecommendation(
            title=book.title,
            author=book.author or "",
            publication_date=(
                book.publication_date.strftime("%Y-%m-%d")
                if book.publication_date
                else ""
            ),
            description=book.description or "",
            genre=book.genre or "",
        )
