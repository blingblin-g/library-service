from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, session
)
import datetime
import sqlite3
from werkzeug.exceptions import abort
from app.auth import login_required
#from app.db import get_db
from app import db
from app.models import Book

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
	#db = get_db()
	#books = db.execute(
	#	'SELECT id, name, publisher, author, published_at, page_count, isbn, description, image_path, stock, rating FROM book'
	#).fetchall()
	books = Book.query.all()
	print("--------------------------------------")
	print(books)
	print("--------------------------------------")
	return render_template('index.html', books=books)

#def is_available(id):
#	db = get_db()
#	print(session['user_id'])
#	ret = db.execute(
#		'SELECT count(book_id) FROM profile WHERE user_id=?', (session['user_id'], )
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
	#db = get_db()
	#stock = db.execute(
	#	'SELECT stock FROM book WHERE id=? AND stock > 0', (id, )
	#).fetchone()
	#is_available = db.execute(
	#	'SELECT book_id FROM profile WHERE user_id=? AND book_id=? AND end_date is NULL', (session['user_id'], id)
	#).fetchone()
	book = Book.query.filter(Book.id==id).first()
	is_available = Profile.query.filter(Profile.user_id == session['user_id'], Profile.book_id == id, Profile.end_date == None).first()
	try:
		if is_available['book_id']:
			flash('이미 대출 중입니다!')
		elif book.stock is None:
			flash('더이상 빌릴 수 있는 책이 없습니다.')
	except:
		#db.execute(
		#	'UPDATE book SET stock = stock - 1 WHERE id=? AND stock > 0', (id, )
		#).fetchone()
		#db.execute(
		#	'INSERT INTO profile (user_id, book_id, start_date) VALUES (?, ?, ?)', (session['user_id'], id, datetime.datetime.now().strftime('%Y-%m-%d'))
		#).fetchone()
		#db.commit()
		book = Book.query.get(Book.id==id).first()
		if book.stock > 0:
			book.stock -= 1
		profile = Profile(user_id=session['user_id'], book_id=id, start_date=datetime.datetime.now().strftime('%Y-%m-%d'))
		db.session.add(profile)
		db.session.commit()
		
	#elif not is_available(id):
	#	flash('You have too many books!')

	return redirect(url_for('index'))
