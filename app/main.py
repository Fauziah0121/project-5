from flask import Flask, jsonify, request
from decouple import config
import psycopg2
from flask_sqlalchemy import SQLAlchemy

DB_URI = f"postgresql+psycopg2://{config('MB_DB_USER')}:{config('MB_DB_PASS')}@{config('MB_DB_HOST')}:{str(config('MB_DB_PORT'))}/{config('MB_DB_DBNAME')}"
app = Flask(_name_)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column('user_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    telp = db.Column(db.String(14))

@app.route("/health")
def health():
    return jsonify({"status": "oke"})

@app.route("/db_check")
def db_check():
    conn_pg = psycopg2.connect(
        host=config('MB_DB_HOST'),
        database=config('MB_DB_DBNAME'),
        user=config('MB_DB_USER'),
        password=config('MB_DB_PASS'),
        port=config('MB_DB_PORT')
    )
    cur = conn_pg.cursor()
    return jsonify({"status": 200, "db": "connected"})

@app.route("/user", methods=["GET", "POST", "PUT", "DELETE"])
def user():
    if request.method == "GET":
        users = Users.query.all()
        results = [{"id": u.id} for u in users] 
        return jsonify(results)
    elif request.method == 'POST':
        user = Users(
            name=request.form['name'],
            city=request.form['city'],
            telp=request.form['telp']
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({"status": "ok"})
    elif request.method == 'PUT':
        user_id = request.form['user_id']
        user = Users.query.filter_by(id=user_id).first()
        if user:
            user.name = request.form.get('name', user.name)
            user.city = request.form.get('city', user.city)
            user.telp = request.form.get('telp', user.telp)
            db.session.commit()
            return jsonify({"status": "ok"})
        else:
            return jsonify({"error": "User not found"}), 404
    elif request.method == 'DELETE':
        user = Users.query.filter_by(id=request.form['user_id']).delete()
        db.session.commit()
        return jsonify({"status": "ok"})
    else:
        return 'METHOD NOT ALLOWED'

@app.route("/user/<int:id>", methods=['GET'])  # Corrected indentation and added int: before id
def user_by_id(id):
    users = Users.query.filter_by(id=id)
    try:
        results = {"id": users.first().id, "name": users.first().name, "city": users.first().city, "telp": users.first().telp}  # Changed list comprehension to direct access
        return jsonify(results)
    except Exception:
        return jsonify({'error': "id not found"})

if _name_ == "_main_":
    app.run(debug=True, host="0.0.0.0")