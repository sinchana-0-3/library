from flask import Blueprint, flash, jsonify, render_template, request, redirect
from .models import Book, User
from .extensions import db

bp = Blueprint('main', __name__)


# -----------------------
# Dashboard
# -----------------------
@bp.route('/')
def home():
    books = Book.query.all()
    return render_template('dashboard.html', books=books)


# -----------------------
# Books Page
# -----------------------
@bp.route('/books')
def books():
    books = Book.query.all()
    return render_template('books.html', books=books)


# -----------------------
# Add Book
# -----------------------
@bp.route('/add_book', methods=['GET', 'POST'])
def add_book():

    if request.method == 'POST':

        title = request.form['title']
        author = request.form['author']

        new_book = Book(
            title=title,
            author=author
        )

        db.session.add(new_book)
        db.session.commit()

        return redirect('/books')

    return render_template('add_book.html')


# -----------------------
# Delete Book
# -----------------------
@bp.route('/delete_book/<int:id>')
def delete_book(id):

    book = Book.query.get(id)

    if book:
        db.session.delete(book)
        db.session.commit()

    return redirect('/books')


# -----------------------
# Users Page
# -----------------------
@bp.route('/users')
def users():
    users = User.query.all()
    return render_template('users.html', users=users)


# -----------------------
# Add User
# -----------------------
@bp.route('/add_user', methods=['GET', 'POST'])
def add_user():

    if request.method == 'POST':

        name = request.form['name']

        new_user = User(name=name)

        db.session.add(new_user)
        db.session.commit()

        return redirect('/users')

    return render_template('add_user.html')


# -----------------------
# Delete User
# -----------------------
@bp.route('/delete_user/<int:id>')
def delete_user(id):

    user = User.query.get(id)

    if user:
        db.session.delete(user)
        db.session.commit()

    return redirect('/users')


# -----------------------
# Issue Book
# -----------------------
@bp.route('/issue', methods=['GET', 'POST'])
def issue_book():

    if request.method == 'POST':

        book_id = request.form['book_id']

        book = Book.query.get(book_id)

        if book:
            book.available = False
            db.session.commit()

            return jsonify({
                'message': 'Book Issued Successfully'
            })

    return render_template('issue.html')


# -----------------------
# Add Sample Data
# -----------------------
@bp.route('/add_sample')
def add_sample():
    sample_books = [
        {'title': 'The Great Gatsby', 'author': 'F. Scott Fitzgerald'},
        {'title': 'To Kill a Mockingbird', 'author': 'Harper Lee'},
        {'title': '1984', 'author': 'George Orwell'},
    ]

    sample_users = [
        {'name': 'Alice'},
        {'name': 'Bob'},
    ]

    # remove exact duplicate book rows
    seen_books = set()
    for book in Book.query.order_by(Book.id).all():
        key = (book.title, book.author)
        if key in seen_books:
            db.session.delete(book)
        else:
            seen_books.add(key)

    # remove exact duplicate user rows
    seen_users = set()
    for user in User.query.order_by(User.id).all():
        if user.name in seen_users:
            db.session.delete(user)
        else:
            seen_users.add(user.name)

    added = False
    for b in sample_books:
        existing_book = Book.query.filter_by(title=b['title'], author=b['author']).first()
        if not existing_book:
            db.session.add(Book(title=b['title'], author=b['author']))
            added = True

    for u in sample_users:
        existing_user = User.query.filter_by(name=u['name']).first()
        if not existing_user:
            db.session.add(User(name=u['name']))
            added = True

    if added:
        flash('Sample data has been added to the library.', 'success')
    else:
        flash('Sample data is already present and duplicate rows were cleaned.', 'info')

    db.session.commit()

    return redirect('/')