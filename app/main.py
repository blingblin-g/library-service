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

#def is_available(id):
#	db = get_db()
#	print(session['user_id'])
#	ret = db.execute(
#		'SELECT count(book_id) as id FROM profile WHERE user_id=?', (session['user_id'], )
#	)
#	ret.row_factory = sqlite3.Row
#	print(f"==============ret:{ret}================")
#	#if ret >= 3:
#	#	print("============================================요기냐?")
#	#	return False
#	for i in ret.fetchall():
#		print(f"=========================={i}========")
#	print("===============================================조기냐?")
#	return True

@bp.route('/checkout', methods=('POST', ))
@login_required
def checkout():
	id = request.form['id']
	db = get_db()
	ret = db.execute(
		'SELECT stock FROM book WHERE id=? AND stock > 0', (id, )
	).fetchone()
	is_available = db.execute(
		'SELECT book_id FROM profile WHERE user_id=? AND book_id=?', (session['user_id'], id)
	).fetchone()
	print(f'====================={id}=====================')
	try:
		if is_available['book_id']:
			flash('이미 빌린 책입니다!')
		elif ret is None:
			flash('There is no book anymore!')
	except:
		db.execute(
			'UPDATE book SET stock = stock - 1 WHERE id=? AND stock > 0', (id, )
		).fetchone()
		db.execute(
			'INSERT INTO profile (user_id, book_id, start_date) VALUES (?, ?, ?)', (session['user_id'], id, datetime.datetime.now().strftime('%Y-%m-%d'))
		).fetchone()
		db.execute(
			'INSERT INTO log (user_id, book_id, start_date) VALUES (?, ?, ?)', (session['user_id'], id, datetime.datetime.now().strftime('%Y-%m-%d'))
		).fetchone()
		
		db.commit()
		
	#elif not is_available(id):
	#	flash('You have too many books!')

	return redirect(url_for('index'))
