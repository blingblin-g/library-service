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
		'SELECT * FROM book JOIN log ON book.id=log.book_id WHERE profile.user_id=?', (session['user_id'], )
	).fetchone()
	#if request.method == 'POST':
	#	댓글 업데이트
	return render_template('book_info.html', book=book)