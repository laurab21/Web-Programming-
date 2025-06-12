import pytest
from sqlalchemy.orm import Session

from src.models.books import Book
from src.repositories.books import BookRepository
from src.services.books import BookService
from src.api.schemas.books import BookCreate, BookUpdate

def test_create_book(db_session: Session):
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Test Book",
        author="Author Name",
        isbn="1234567890",
        quantity=5
    )

    book = service.create(obj_in=book_in)

    assert book.title == "Test Book"
    assert book.author == "Author Name"
    assert book.isbn == "1234567890"
    assert book.quantity == 5

def test_update_book(db_session: Session):
    repository = BookRepository(Book, db_session)
    service = BookService(repository)

    book_in = BookCreate(
        title="Original Book",
        author="Author Name",
        isbn="0987654321",
        quantity=3
    )

    book = service.create(obj_in=book_in)

    # Update title
    book_update = BookUpdate(title="Updated Book")
    updated_book = service.update(db_obj=book, obj_in=book_update)

    assert updated_book.title == "Updated Book"
    assert updated_book.author == "Author Name"
    assert updated_book.isbn == "0987654321"
    assert updated_book.quantity == 3
