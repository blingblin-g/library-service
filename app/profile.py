from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
	db = get_db()
	books = db. execute(
		'SELECT * FROM book JOIN profile ON book.id=profile.book_id WHERE profile.user_id=?', (session['user_id'], )
	).fetchall()
	return render_template('profile.html', books=books)