from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('log', __name__, url_prefix='/log')

@bp.route('/profile', methods=('GET', 'POST'))
def log(id):
	db = get_db()
	book = db.execute(
		'SELECT * FROM book JOIN log ON book.id=log.book_id WHERE log.user_id=?', (session['user_id'], )
	).fetchone()
	return render_template('book_info.html', logs=logs)