from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import desc
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'crud.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
	id 			= db.Column(db.Integer, primary_key=True)
	first_name	= db.Column(db.String(80))
	last_name	= db.Column(db.String(80))
	company_name= db.Column(db.String(80))
	age			= db.Column(db.Integer)
	city		= db.Column(db.String(80))
	state		= db.Column(db.String(80))
	zip			= db.Column(db.Integer)
	email		= db.Column(db.String(80))
	web			= db.Column(db.String(80))


	def __init__(self, *args, **kwargs):
		self.id = kwargs["id"]
		self.first_name = kwargs["first_name"]
		self.last_name = kwargs["last_name"]
		self.company_name = kwargs["company_name"]
		self.age = kwargs["age"]
		self.city = kwargs["city"]
		self.state = kwargs["state"]
		self.zip = kwargs["zip"]
		self.email = kwargs["email"]
		self.web = kwargs["web"]

class UserSchema(ma.Schema):
	class Meta:
		fields=('id','first_name','last_name',
				'company_name','age','city',
				'state','zip','email','web')
user_schema  = UserSchema()
users_schema = UserSchema(many=True)

@app.route('/api/users/', methods=["GET","POST"])
def create_or_retrieve():
	if request.method=="GET":
		limit = 5
		page_no = 1
		sort = "id"
		name = request.args.get('name')
		order = 1
		if 'page' in request.args:
			page_no = request.args.get('page', type = int)
		
		if 'limit' in request.args:
			limit = request.args.get('limit', type = int)

		if 'sort' in request.args:
			sort = request.args.get('sort')
			if '-' in sort:
				sort = sort.replace("-","")
				order = 2
		if 'name' in request.args:
			if  order==1:
				all_users = User.query.filter(User.first_name.ilike(f'%{name}%')
										|User.last_name.ilike(f'%{name}%')).order_by(sort).paginate(page_no,limit,False).items
			else:
				all_users = User.query.filter(User.first_name.ilike(f'%{name}%')
										|User.last_name.ilike(f'%{name}%')).order_by(desc(sort)).paginate(page_no,limit,False).items
		else:
			if  order==1:
				all_users = User.query.order_by(sort).paginate(page_no,limit,False).items
			else:
				all_users = User.query.order_by(desc(sort)).paginate(page_no,limit,False).items

		receieved_data = users_schema.dump(all_users)
		return jsonify(receieved_data.data)
	elif request.method=="POST":
		id				= request.json['id']
		first_name		= request.json['first_name']
		last_name		= request.json['last_name']
		company_name	= request.json['company_name']
		age				= request.json['age']
		city			= request.json['city']
		state			= request.json['state']
		zip				= request.json['zip']
		email			= request.json['email']
		web				= request.json['web']

		new_user = User(id = id,first_name = first_name,last_name = last_name,
						company_name = company_name, age = age, city = city,
						state = state, zip = zip, email = email, web = web)

		db.session.add(new_user)
		db.session.commit()
		return ('',201)
		# return user_schema.jsonify(new_user),201

@app.route('/api/users/<id>', methods=["GET","PUT","DELETE"])
def update(id):
	if request.method=="GET":
		obj = User.query.get(id)
		received = user_schema.dump(obj)
		return jsonify(received.data)
	elif request.method=="PUT":
		obj = User.query.get(id)
		req_data = request.get_json()
		# print(req_data)
		if 'first_name' in req_data:
			obj.first_name		= request.json['first_name']
		if 'last_name' in req_data:
			obj.last_name		= request.json['last_name']
		if 'company_name' in req_data:
			obj.company_name		= request.json['company_name']
		if 'age' in req_data:
			obj.age		= request.json['age']
		if 'city' in req_data:
			obj.city		= request.json['city']
		if 'state' in req_data:
			obj.state		= request.json['state']
		if 'zip' in req_data:
			obj.zip		= request.json['zip']
		if 'email' in req_data:
			obj.email		= request.json['email']
		if 'web' in req_data:
			obj.web		= request.json['web']
		db.session.commit()
		return user_schema.jsonify(obj)
	elif request.method=="DELETE":
		obj = User.query.get(id)
		db.session.delete(obj)
		db.session.commit()
		return ('',200)

if __name__ == "__main__":
    app.run(debug=True)