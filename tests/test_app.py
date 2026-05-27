from app import create_app
from app.models import Book, User


def test_home_page():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    client = app.test_client()

    response = client.get('/')

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
