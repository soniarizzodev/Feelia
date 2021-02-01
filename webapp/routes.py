"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from webapp import app

from webapp.User import User
from webapp.UsersManager import UsersManager

from webapp.api.get_book import get_book
from webapp.api.update_book_entry import update_book_entry
from webapp.api.delete_book_entry import delete_book_entry

from webapp.const import ERROR_MISSING_PARAMS


@app.route('/login_page', methods=['GET', 'POST'])
def login_page():
    """Login Page"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    return render_template(
        'login.html',
        title='Accedi',
        year=datetime.now().year,
    )

@app.route('/')
@app.route('/home')
def home():
    """Renders the landing page."""
    return render_template(
        'home.html',
        title='Feelia - Together for your special moments',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

################################################
## WEB SERVICES

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    data = request.form
    
    user = User(data['username'], data['password'])
    users_manager = UsersManager(user)

    if users_manager.check():
        login_user(user, True)
        return redirect(url_for('home'))
    else:
        return redirect(url_for('login_page', failed = True))


@app.route('/book')
@login_required
def book():    
    """Returns the book content."""
    return get_book(current_user)


@app.route('/updatebookentry', methods=['GET', 'POST'])
@login_required
def updatebookentry():    
    """Adds or updates a book entry"""
    media = request.files
    book_entry = request.form.get('book_entry')

    if book_entry is not None:
        return update_book_entry(book_entry, media)
    else:
        response = Response(False, ERROR_MISSING_PARAMS)
        return response.compose()


@app.route('/deletebookentry', methods=['GET', 'POST'])
@login_required
def deletebookentry():    
    """Deletes a book entry"""
    data = request.get_json(force=True)

    if (data is not None) and ('book_entry_id' in data) and ('edit_key' in data):
        return delete_book_entry(data['book_entry_id'], data['edit_key'])
    else:
        response = Response(False, ERROR_MISSING_PARAMS)
        return response.compose()