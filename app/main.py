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

#@bp.route('/create', methods=('GET', 'POST'))
#@login_required
#def create():
#	if request.method == 'POST':
#		title = request.form['title']
#		body = request.form['body']
#		error = None
#		if not title:
#			error = 'Title is required.'
#		if error is not None:
#			flash(error)
#		else:
#			db = get_db()
#			db.execute(
#				'INSERT INTO post (title, body, author_id)'
#				' VALUES (?, ?, ?)',
#				(title, body, g.user['id'])
#			)
#			db.commit()
#			return redirect(url_for('blog.index'))
#	return render_template('blog/create.html')

#def get_post(id, check_author=True):
#	post = get_db().execute(
#		'SELECT p.id, title, body, created, author_id, username'
#		' FROM post p JOIN user u ON p.author_id = u.id'
#		' WHERE p.id = ?',
#		(id,)
#	).fetchone()
#	if post is None:
#		abort(404, "Post id {0} doesn't exist.".format(id))
#	if check_author and post['author_id'] != g.user['id']:
#		abort(403)
#	return post

#@bp.route('/<int:id>/update', methods=('GET', 'POST'))
#@login_required
#def update(id):
#	post = get_post(id)
#	if request.method == 'POST':
#		title = request.form['title']
#		body = request.form['body']
#		error = None
#		if error is not None:
#			flash(error)
#		else:
#			db = get_db()
#			db.execute(
#				'UPDATE post SET title = ?, body = ?'
#				' WHERE id = ?',
#				(title, body, id)
#			)
#			db.commit()
#			return redirect(url_for('blog.index'))
#	return render_template('blog/update.html', post=post)

#@bp.route('/<int:id>/delete', methods=('POST',))
#@login_required
#def delete(id):
#	get_post(id)
#	db = get_db()
#	db.execute('DELETE FROM post WHERE id = ?', (id,))
#	db.commit()
#	return redirect(url_for('blog.index'))