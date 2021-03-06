from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for, session
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

import datetime

bp = Blueprint('book_info', __name__, url_prefix='/book_info')

@bp.route('/<id>', methods=('GET', 'POST'))
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

#	댓글을 썼을 때 C
	#	이미 썼는지 한 번 확인을 하고, 안썼으면 새로 쓰고(INSERT INTO), 데이터가 있으면 쓰지 말라고 한다.
	#	내용이 있는지 확인 후 없으면 내용을 채우라고 돌려보냄
@bp.route('/create', methods=('GET', 'POST'))
def create_comment():
	id = request.form['id']
	
	db = get_db()
	print(session['user_id'])
	try:
		is_available = db.execute(
			'SELECT author_id, book_id, created, body, star FROM comments WHERE author_id=?', (session['user_id'], )
		).fetchone()
	except:
		flash("이미 댓글을 달았습니다!")
		return (redirect(url_for('book_info.book_info', id=id)))

	body = request.form['body']
	star = request.form['rating']

	error = error_handling(body, star)
	if error is not None:
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
			'UPDATE book SET rating=? WHERE id=?', (avg_star[0], id)
		)
		db.commit()
		#comments = Comments(author_id=session['user_id'], book_id=id, title=title, body=body, date=datetime.datetime.now().strftime('%Y-%m-%d'), star=star)
		#db.session.add(comments)
		#db.session.commit()
	return redirect(url_for('book_info.book_info', id = id))


@bp.route('/update', methods=('GET', 'POST'))
#	댓글을 업데이트 했을 때 U
	#	프론트에서 댓글이 있을 경우에만 옆에다가 수정(crystal 아님) 버튼이 뜨는거죠 (POST)
	#	받아와서, 걔가 내용이 있는지 확인 후 없으면 내용 채우라고 돌려보냄
def update_comment():
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
		#comment = Comments.query.get(Comment.book_id==id)
		#comment.title = title
		#comment.body = body
		#comment.star = star
		#comment.date = datetime.datetime.now().strftime('%Y-%m-%d')
		#db.session.commit()

#	댓글을 지웠을 때 D
	#	프론트에서 댓글이 있을 경우에만 옆에다가 삭제 버튼이 뜨는거죠 (POST)
@bp.route('/delete', methods=('GET', 'POST'))
def delete_comment():
	id = request.form['delete']
	db = get_db()
	db.execute(
		'DELETE FROM comments WHERE book_id=? AND author_id=?', (id, session['user_id'])
	)
	avg_star = db.execute(
		'SELECT AVG(star) FROM comments WHERE book_id=?', (id, )
	).fetchone()
	print("---------------------------here=======================================")
	for i in avg_star:
		print(i)
	print("---------------------------or here=======================================")
	db.execute(
		'UPDATE book SET rating=? WHERE id=?', (avg_star[0], id)
	).fetchone()
	db.commit()
	#comment = Comments.query.get(Comments.book_id==id, Comments.user_id==session['user_id'])
	#db.session.delete(comment)
	#db.session.commit()
	return redirect(url_for('book_info.book_info', id = id))
