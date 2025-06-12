import pytest
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from src.models.loans import Loan
from src.models.books import Book
from src.models.users import User
from src.repositories.loans import LoanRepository
from src.repositories.books import BookRepository
from src.repositories.users import UserRepository
from src.services.loans import LoanService
from src.api.schemas.books import BookCreate
from src.api.schemas.users import UserCreate

def create_user_and_book(db_session):
    user_repository = UserRepository(User, db_session)
    book_repository = BookRepository(Book, db_session)

    user_in = UserCreate(
        email="loanuser@example.com",
        password="password123",
        full_name="Loan User"
    )
    user = user_repository.create(obj_in={
        "email": user_in.email,
        "hashed_password": "hashedpassword",
        "full_name": user_in.full_name,
        "is_active": True,
        "is_admin": False
    })

    book_in = BookCreate(
        title="Loan Book",
        author="Author",
        isbn="1234567890",
        quantity=3
    )
    book = book_repository.create(obj_in=book_in)

    return user, book

def test_create_loan(db_session: Session):
    loan_repository = LoanRepository(Loan, db_session)
    book_repository = BookRepository(Book, db_session)
    user_repository = UserRepository(User, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    user, book = create_user_and_book(db_session)

    loan = service.create_loan(user_id=user.id, book_id=book.id, loan_period_days=7)

    assert loan.user_id == user.id
    assert loan.book_id == book.id
    assert loan.return_date is None
    assert loan.due_date.date() == (datetime.utcnow() + timedelta(days=7)).date()

def test_return_loan(db_session: Session):
    loan_repository = LoanRepository(Loan, db_session)
    book_repository = BookRepository(Book, db_session)
    user_repository = UserRepository(User, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    user, book = create_user_and_book(db_session)

    loan = service.create_loan(user_id=user.id, book_id=book.id)
    returned_loan = service.return_loan(loan_id=loan.id)

    assert returned_loan.return_date is not None

def test_extend_loan(db_session: Session):
    loan_repository = LoanRepository(Loan, db_session)
    book_repository = BookRepository(Book, db_session)
    user_repository = UserRepository(User, db_session)
    service = LoanService(loan_repository, book_repository, user_repository)

    user, book = create_user_and_book(db_session)

    loan = service.create_loan(user_id=user.id, book_id=book.id)
    extended_loan = service.extend_loan(loan_id=loan.id, extension_days=7)

    assert extended_loan.due_date > loan.due_date
