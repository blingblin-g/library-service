# flask에서 사용하는 대표적인 orm을 가지고 로그인 기능을 구현해보아요 :)
# flask에서 주로 사용되는 jija도 간단히 살펴봅시다.

from flask import Flask, request, jsonify, url_for, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bee11777d0d22065bdb8fc7edafb0557'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
db.create_all()


class User(db.Model):
    __table_name__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/profile')
def profile():
    return render_template("profile.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid user info")
            return redirect(url_for('login'))

        return redirect(url_for("profile"))
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    return "logout"


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('name')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email address already exists")
            return redirect(url_for('signup'))

        new_user = User(email=email, username=username,
                        password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))
    else:
        return render_template("signup.html")


if __name__ == '__main__':
    app.run(debug=True)
