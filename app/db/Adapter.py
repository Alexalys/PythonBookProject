from app.models.Book import BookModel
from app.schemas.bookSchema import BookRecommendation


class BasicAdapter:

    def to_data_source(self, book: BookModel) -> BookRecommendation:
        return BookRecommendation(
            title=book.title,
            author=book.author or "",  # Handle potential None value for author
            publication_date=(
                book.publication_date.strftime("%Y-%m-%d")
                if book.publication_date
                else ""
            ),
            description=book.description
            or "",  # Handle potential None value for description
            genre=book.genre or "",  # Handle potential None value for genre
        )
