from flask import (
	Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('profile', __name__)

@bp.route('/profile', methods=('GET', 'POST'))
def profile():
	# db = get_db()
	# 여기서 user랑 book table join 한거 들쑤셔서 user가 빌린 책 찾아낸다
	# 반납하기 버튼 누르면 삭제한다.
	return render_template('profile.html')