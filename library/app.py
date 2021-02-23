from flask import Flask, render_template, request, url_for, redirect, jsonify

app = Flask(__name__)

@app.route('/')
def home():
	titles = ['elice flask class day1', 'beautifulsoup is beautiful!']
	return render_template("home.html", titles=titles)

@app.route('/user/<user_id>')
def user(user_id):
	print(user_id)
	return render_template("index.html", user_id=user_id)

@app.route('/elice')
def elicer():
	return "Hello elice"

@app.route('/register', methods=["POST"])
def register():
	username = request.form['user_id']
	password = request.form['user_pw']
	print(username, password)
	return "Registered!"


if __name__ == "__main__":
	app.run(debug=True)