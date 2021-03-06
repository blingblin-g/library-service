DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS book;
DROP TABLE IF EXISTS profile;
DROP TABLE IF EXISTS log;

CREATE TABLE user (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
  email TEXT UNIQUE NOT NULL,
	username TEXT NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE post (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES user (id)
);

CREATE TABLE book (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  publisher TEXT NOT NULL,
  author TEXT NOT NULL,
  published_at DATETIME NOT NULL,
  page_count INTEGER NOT NULL,
  isbn INTEGER NOT NULL,
  description TEXT NOT NULL,
  image_path TEXT NOT NULL,
  stock INTEGER NOT NULL,
  rating INTEGER NOT NULL
);

CREATE TABLE profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  book_id INTEGER NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE DEFAULT NULL,

  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (book_id) REFERENCES book (id)
);