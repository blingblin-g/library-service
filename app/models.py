from app import db
from datetime import datetime

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	email = db.Column(db.Text(), nullable=False)
	username = db.Column(db.Text(), nullable=False)
	password = db.Column(db.Text(), nullable=False)

class Comments(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
	title = db.Column(db.Text(), nullable=False)
	body = db.Column(db.Text(), nullable=False)
	date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	star = db.Column(db.Integer, nullable=False)

class Profile(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
	start_date = db.Column(db.DateTime, nullable=False)
	end_date = db.Column(db.DateTime, nullable=False)

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.Text(), nullable=False)
	publisher = db.Column(db.Text(), nullable=False)
	author = db.Column(db.Text(), nullable=False)
	published_at = db.Column(db.DateTime, nullable=False)
	page_count = db.Column(db.Integer(), nullable=False)
	isbn = db.Column(db.Integer(), nullable=False)
	description = db.Column(db.Text(), nullable=False)
	image_path = db.Column(db.Text(), nullable=False)
	stock = db.Column(db.Integer(), nullable=False)
	rating = db.Column(db.Integer(), nullable=False)
