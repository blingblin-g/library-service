from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('book_info', __name__, url_prefix='/book_info')

@bp.route('/<id>', methods=('GET', 'POST'))
def book_info(id):
	db = get_db()
	book = db.execute(
		'SELECT id, name, publisher, author, published_at, page_count, isbn, description, image_path, stock, rating FROM book WHERE id = ?', (id, )
	).fetchone()
	#if request.method == 'POST':
	#	댓글 업데이트
	return render_template('book_info.html', book=book)