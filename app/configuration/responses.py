post_responses = {
    201: {
        "description": "Book created successfully",
        "content": {
            "application/json": {
                "example": {
                    "uuid": "123e4567-e89b-12d3-a456-426614174000",
                    "title": "Great Expectations",
                    "author": "Charles Dickens",
                    "publication_date": "1949-06-08",
                    "description": "A dystopian novel.",
                    "genre": "Dystopian",
                }
            }
        },
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {"detail": "An error occurred while creating the book"}
            }
        },
    },
}

get_response = {
    200: {
        "description": "Returned a book",
        "content": {
            "application/json": {
                "example": {
                    "uuid": "12345",
                    "title": "Example Book",
                    "author": "John Doe",
                    "publication_date": "2023-01-01",
                    "description": "A sample book",
                    "genre": "Fiction",
                }
            }
        },
    },
    404: {"description": "Book not found"},
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {"detail": "An error occurred while reading a book"}
            }
        },
    },
}

get_responses = {
    200: {
        "description": "Returned books",
        "content": {
            "application/json": {
                "example": [
                    {
                        "uuid": "12345",
                        "title": "Example Book",
                        "author": "John Doe",
                        "publication_date": "2023-01-01",
                        "description": "A sample book",
                        "genre": "Fiction",
                    }
                ]
            }
        },
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {"detail": "An error occurred while reading books"}
            }
        },
    },
}

delete_response = {
    204: {
        "description": "Successfuly deleted",
        "content": {},
    },
    404: {
        "description": "Book not Found",
        "content": {"application/json": {"example": {"detail": "Book is not found"}}},
    },
    500: {
        "description": "Internal Server Error",
        "content": {
            "application/json": {
                "example": {"detail": "An error occurred while reading books"}
            }
        },
    },
}
