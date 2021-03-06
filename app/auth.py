import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
from app.models import User
from app import db

#from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		email = request.form['email']
		username = request.form['username']
		password = request.form['password']
		password_check = request.form['password-check']
		#db = get_db()
		error = None

		# error handling
		if not email:
			error = 'Email is required.'
		elif not username:
			error = 'Username is required.'
		elif not password:
			error = 'Password is required.'
		elif len(password) < 8:
			error = 'Password is too short.'
		elif password != password_check:
			error = 'Password is incorrect.'
		elif User.query.filter(User.email==email).first():
		#elif db.execute(
		#	'SELECT id FROM user WHERE email = ?', (email, )
		#).fetchone() is not None:
			error = 'User {} is already registered.'.format(email)
		if error is None:
			#db.execute(
			#	'INSERT INTO user (email, username, password) VALUES (?, ?, ?)', (email, username, generate_password_hash(password))
			#)
			#db.commit()
			data = User(email=email, username=username, password=generate_password_hash(password))
			db.session.add(data)
			db.session.commit()
			return redirect(url_for('auth.login'))
		flash(error)
	return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		email = request.form['email']
		password = request.form['password']
		#db = get_db()
		error = None
		#user = db.execute(
		#	'SELECT * FROM user WHERE email = ?', (email,)
		#).fetchone()
		user = User.query.filter(User.email == email).first()
		print("-----------------------")
		print(user)
		print("-----------------------")
		if user is None:
			error = 'Incorrect username.'
		elif not check_password_hash(user.password, password):
			error = 'Incorrect password.'
		
		if error is None:
			session.clear()
			session['user_id'] = user.id
			return redirect(url_for('index'))
		
		flash(error)

	return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')

	if user_id is None:
		g.user = None
	else:
		g.user = User.query.filter(User.id==user_id).first()
		#g.user = get_db().execute(
		#	'SELECT * FROM user WHERE id = ?', (user_id,)
		#).fetchone()

@bp.route('/logout')
def logout():
	session.clear()
	return redirect(url_for('index'))

def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
		if g.user is None:
			return redirect(url_for('auth.login'))

		return view(**kwargs)
		
	return wrapped_view