from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class Note(db.Model):
 	id 		= db.Column(db.Integer, primary_key=True)
 	title 	= db.Column(db.String(80))
 	body	= db.Column(db.Text)

 	def __init__(self, title, body):
 		 self.title = title
 		 self.body = body

class NoteSchema(ma.Schema):
	class Meta:
		fields=('id','title','body')

note_schema  = NoteSchema()
notes_schema = NoteSchema(many=True)

@app.route('/notes/create', methods=["POST"])
def create():
		title 	= request.json['title']
		body	= request.json['body']


		new_note = Note(title=title,body=body)

		db.session.add(new_note)
		db.session.commit()

		return note_schema.jsonify(new_note)

@app.route('/notes/')
def retrieve():
	all_notes = Note.query.all()
	receieved_data = notes_schema.dump(all_notes)
	return jsonify(receieved_data.data)

@app.route('/notes/update/<id>', methods=["POST"])
def update(id):
	if request.method=="POST":
		obj = Note.query.get(id)
		title = request.json["title"]
		body  = request.json["body"]

		obj.title = title
		obj.body = body

		db.session.commit()
		return note_schema.jsonify(obj)

@app.route('/notes/delete/<id>', methods=['DELETE'])
def delete(id):
	note = Note.query.get(id)
	db.session.delete(note)
	db.session.commit()
	return note_schema.jsonify(note)

if __name__ == "__main__":
    app.run(debug=True)