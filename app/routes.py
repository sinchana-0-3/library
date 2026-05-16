from flask import Blueprint, jsonify, render_template, request, redirect
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