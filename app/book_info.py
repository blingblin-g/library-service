from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

import datetime

bp = Blueprint('book_info', __name__, url_prefix='/book_info')

@bp.route('/<id>', methods=('GET', 'POST'))
@login_required
def book_info(id):
	db = get_db()
	book = db.execute(
		'SELECT * FROM book WHERE id = ?', (id, )
	).fetchone()
	comments = db.execute(
		'SELECT * FROM comments JOIN user ON comments.author_id=user.id WHERE book_id = ?', (id, )
	)	
	return render_template('book_info.html', book=book, comments=comments)

def error_handling(body, star):
	if body is None:
		return '내용을 입력해주세요.'
	elif star is None:
		return '평점을 입력해주세요.'
	return None

@bp.route('/<id>/create', methods=('GET', 'POST'))
def create_comment(id):
	db = get_db()
	try:
		db.execute(
			'SELECT author_id, book_id, created, body, star FROM comments WHERE author_id=?', (session['user_id'], )
		).fetchone()
	except:
		flash("이미 댓글을 달았습니다!")
		return (redirect(url_for('book_info.book_info', id=id)))

	body = request.form['body']
	star = request.form.get('rating')
	error = error_handling(body, star)
	if error:
		flash(error)
	else:
		db.execute(
			'INSERT INTO comments (author_id, book_id, body, created, star) VALUES (?, ?, ?, ?, ?)',
			(session['user_id'], id, body, datetime.datetime.now().strftime('%Y-%m-%d'), star)
		).fetchone()
		avg_star = db.execute(
			'SELECT AVG(star) FROM comments WHERE book_id=?', (id, )
		).fetchone()
		db.execute(
			'UPDATE book SET rating=? WHERE id=?', (round(avg_star[0], 1), id)
		)
		db.commit()
	return redirect(url_for('book_info.book_info', id = id))


@bp.route('/<id>/update', methods=('GET', 'POST'))
def update_comment(id, comment_id):
	body = request.form['body']
	start = request.form['star']
	id = request.form['edit']

	error = error_handling(body, star)
	if error is not None:
		flash(error)
	else:
		db = get_db()
		db.execute(
			'UPDATE comments SET body=?, star=? WHERE book_id=? AND author_id=?', (body, star, id, session['user_id'])
		).fetchone()
		avg_star = db.execute(
			'SELECT AVG(star) FROM comments WHERE book_id=?', (id, )
		).fetchone()
		db.execute(
			'UPDATE book SET rating=? WHERE book_id=?', (avg_star, id)
		).fetchone()
		db.commit()
	
	return redirect(url_for('book_info.book_info', id = id))

@bp.route('/<id>/delete/<comment_id>', methods=('GET', 'POST'))
def delete_comment(id, comment_id):
	db = get_db()
	db.execute(
		'DELETE FROM comments WHERE id=?', (comment_id,)
	)
	avg_star = db.execute(
		'SELECT AVG(star) FROM comments WHERE book_id=?', (id, )
	).fetchone()
	db.execute(
		'UPDATE book SET rating=? WHERE id=?', (round(avg_star[0], 1), id)
	).fetchone()
	db.commit()
	return redirect(url_for('book_info.book_info', id = id))
