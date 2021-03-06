from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('book_info', __name__, url_prefix='/book_info')

@bp.route('/<id>', methods=('GET', 'POST'))
def book_info(id):
	#db = get_db()
	#book = db.execute(
	#	'SELECT id, name, publisher, author, published_at, page_count, isbn, description, image_path, stock, rating FROM book WHERE id = ?', (id, )
	#).fetchone()
	book = Book.query.get(Book.id==id).first()
	#if request.method == 'GET':
	#	댓글이 보여져야함 R
	return render_template('book_info.html', book=book)

def error_handling(title, body, star):
	if title is None:
		return '제목을 작성해주세요.'
	elif body is None:
		return '내용을 입력해주세요.'
	elif star is None:
		return '평점을 입력해주세요.'
	return None

#	댓글을 썼을 때 C
	#	이미 썼는지 한 번 확인을 하고, 안썼으면 새로 쓰고(INSERT INTO), 데이터가 있으면 쓰지 말라고 한다.
	#	내용이 있는지 확인 후 없으면 내용을 채우라고 돌려보냄
def create_comment(id):
	title = request.form.get['title']
	body = request.form.get['body']
	star = request.form.get['star']

	error = error_handling(title, body, star)
	if error is not None:
		flash(error)
	else:
		comments = Comments(author_id=session['user_id'], book_id=id, title=title, body=body, date=datetime.datetime.now().strftime('%Y-%m-%d'), star=star)
		db.session.add(comments)
		db.session.commit()
	return redirect(url_for['book_iinfo'], comments=comments)

#	댓글을 업데이트 했을 때 U
	#	프론트에서 댓글이 있을 경우에만 옆에다가 수정(crystal 아님) 버튼이 뜨는거죠 (POST)
	#	받아와서, 걔가 내용이 있는지 확인 후 없으면 내용 채우라고 돌려보냄
def update_comment(id):
	title = request.form.get['title']
	body = request.form.get['body']
	start = request.form.get['star']

	error = error_handling(title, body, star)
	if error is not None:
		flash(error)
	else:
		comment = Comments.query.get(Comment.book_id==id)
		comment.title = title
		comment.body = body
		comment.star = star
		comment.date = datetime.datetime.now().strftime('%Y-%m-%d')
		db.session.commit()

def delete_comment(id):
	comment = Comments.query.get(Comments.book_id==id, Comments.user_id==session['user_id'])
	db.session.delete(comment)
	db.session.commit()
#	댓글을 지웠을 때 D
	#	프론트에서 댓글이 있을 경우에만 옆에다가 삭제 버튼이 뜨는거죠 (POST)
