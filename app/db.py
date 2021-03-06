import sqlite3
import csv
import click
from flask import current_app, g
from flask.cli import with_appcontext
from datetime import date, datetime

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def init_db():
	db = get_db()
	with current_app.open_resource('schema.sql') as f:
		db.executescript(f.read().decode('utf8'))
	
	with open('./app/static/books.csv', 'r') as f:
		reader = csv.DictReader(f)
		for row in reader:
			published_at = datetime.strptime(row['publication_date'], '%Y-%m-%d').date()
			image_path = f"static/images/{row['id']}"
			print(image_path)
			try:
				fd = open(f'./app/{image_path}.png')
				image_path += '.png'
				fd.close()
			except:
				image_path += '.jpg'
			db = get_db()
			db.execute(
				'INSERT INTO book (id, name, publisher, author, published_at, page_count, isbn, description, image_path, stock, rating)'
				' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
				(int(row['id']), row['book_name'], row['publisher'], row['author'], published_at, int(row['pages']), row['isbn'], row['description'], image_path, 5, 0)
			)
			db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()