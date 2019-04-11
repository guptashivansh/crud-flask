from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'app.sqlite')
db = SQLAlchemy(app)

class Note(db.Model):
 	id 		= db.Column(db.Integer, primary_key=True)
 	title 	= db.Column(db.String(80))
 	body	= db.Column(db.Text)

 	def __init__(self, title, body):
 		 self.title = title
 		 self.body = body

@app.route('/')
def home():
	return render_template("home.html")

@app.route('/notes/create', methods=["POST","GET"])
def create():
	if request.method=="GET":
		return render_template("create_note.html")
	else:
		title 	= request.form["title"]
		body	= request.form["body"]

		note = Note(title=title,body=body)

		db.session.add(note)
		db.session.commit()

		return redirect("/notes/")

@app.route('/notes/')
def retrieve():
	receieved_data = Note.query.all()
	return render_template("display.html", data = receieved_data)

@app.route('/notes/update/<id>', methods=["POST","GET"])
def update(id):
	if request.method=="POST":
		obj = Note.query.get(id)
		title = request.form["title"]
		body  = request.form["body"]
		obj.title = title
		obj.body = body
		db.session.commit()
		return redirect("/notes"	)
	else:
		note = Note.query.get(id)
		return render_template("update_note.html", note = note)

@app.route('/notes/delete/<id>')
def delete(id):
	note = Note.query.get(id)
	db.session.delete(note)
	db.session.commit()
	return redirect('/notes/')

if __name__ == "__main__":
    app.run(debug=True)