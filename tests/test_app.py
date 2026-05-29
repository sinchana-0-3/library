from app import create_app
from app.extensions import db
from app.models import Book, User


def test_home_page():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    client = app.test_client()

    response = client.get('')

    assert response.status_code == 200


def test_add_sample_data_creates_records_once():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    client = app.test_client()

    response = client.get('/add_sample')
    assert response.status_code == 302
    assert response.location.endswith('/')

    with app.app_context():
        books = Book.query.filter(Book.title.in_([
            'The Great Gatsby',
            'To Kill a Mockingbird',
            '1984'
        ])).all()
        users = User.query.filter(User.name.in_(['Alice', 'Bob'])).all()

        assert len(books) == 3
        assert len(users) == 2

    response = client.get('/add_sample')
    assert response.status_code == 302

    with app.app_context():
        books = Book.query.filter(Book.title.in_([
            'The Great Gatsby',
            'To Kill a Mockingbird',
            '1984'
        ])).all()
        users = User.query.filter(User.name.in_(['Alice', 'Bob'])).all()

        assert len(books) == 3
        assert len(users) == 2


def test_return_book_sets_available_true():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    client = app.test_client()

    with app.app_context():
        book = Book(title='Dune', author='Frank Herbert', available=False)
        db.session.add(book)
        db.session.commit()
        book_id = book.id

    response = client.get(f'/return_book/{book_id}')
    assert response.status_code == 302
    assert response.location.endswith('/books')

    with app.app_context():
        returned_book = Book.query.get(book_id)
        assert returned_book.available is True
