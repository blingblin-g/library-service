from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db
import datetime

bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
	#db = get_db()
	#books = db.execute(
	#	'SELECT * FROM book JOIN profile ON book.id=profile.book_id WHERE profile.user_id=?', (session['user_id'], )
	#).fetchall()
	profile = Profile.query.filter(Profile.user_id == session['user_id'])
	books = Book.query.filter(Book.id == profile.book_id)
	return render_template('profile.html', books=books)

@bp.route('/return', methods=('GET', 'POST'))
@login_required
def return_book():
	id = request.form['id']
	#db = get_db()
	#db.execute(
	#	'UPDATE book SET stock = stock + 1 WHERE id=?', (id, )
	#).fetchone()
	#db.execute(
	#	'UPDATE profile SET end_date=? WHERE book_id=? AND user_id=?', (datetime.datetime.now().strftime('%Y-%m-%d'), id, session['user_id'])
	#).fetchone()
	#db.commit()
	book = Book.query.get(Book.id==id).first()
	if book.stock > 0:
		book.stock += 1
	profile = Profile(user_id=session['user_id'], book_id=id, end_date=datetime.datetime.now().strftime('%Y-%m-%d'))
	db.session.add(profile)
	db.session.commit()
	return redirect(url_for('profile'))