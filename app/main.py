from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, session
)
import datetime
import sqlite3
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
	db = get_db()
	books = db.execute(
		'SELECT id, name, publisher, author, published_at, page_count, isbn, description, image_path, stock, rating FROM book'
	).fetchall()
	return render_template('index.html', books=books)

@bp.route('/checkout', methods=('POST', ))
@login_required
def checkout():
	id = request.form['id']
	db = get_db()
	stock = db.execute(
		'SELECT stock FROM book WHERE id=? AND stock > 0', (id, )
	).fetchone()
	is_available = db.execute(
		'SELECT book_id FROM profile WHERE user_id=? AND book_id=? AND end_date is NULL', (session['user_id'], id)
	).fetchone()
	try:
		if is_available['book_id']:
			flash('이미 대출 중입니다!')
		elif stock is None:
			flash('더이상 빌릴 수 있는 책이 없습니다.')
	except:
		db.execute(
			'UPDATE book SET stock = stock - 1 WHERE id=? AND stock > 0', (id, )
		).fetchone()
		db.execute(
			'INSERT INTO profile (user_id, book_id, start_date) VALUES (?, ?, ?)', (session['user_id'], id, datetime.datetime.now().strftime('%Y-%m-%d'))
		).fetchone()
		db.commit()
		
	#elif not is_available(id):
	#	flash('You have too many books!')

	return redirect(url_for('index'))
