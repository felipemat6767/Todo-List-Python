import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Tasks
from flask_migrate import Migrate


Basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(Basedir, "test.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ENV"] = "developement"
app.config["Debug"] = True

Migrate(app, db)
db.init_app(app)

@app.route("/")
def Home():
  return jsonify("H")


@app.route("/tasks", methods = ["POST", "GET"])
def tasks():
    if request.method == "GET":
        tasks = Tasks.query.all()
        if tasks is None:
            return jsonify(error = "Usuario No encontrado"), 400
        results = list(map(lambda tasks: tasks.serialize(), tasks))
        return jsonify(results)
    
    if request.method == "POST":
        tasks = Tasks()
        tasks.label = request.json.get("label")
        tasks.done = request.json.get("done")
        
        if tasks.label == "":
             return jsonify(error = "Falta informacion"), 400
        if tasks.done == "":
            return jsonify(error = "Falta informacion"), 400
        
        db.session.add(tasks)
        db.session.commit()
        return jsonify(tasks.serialize()), 200
    
@app.route("/tasks/<int:id>", methods = ["GET", "DELETE"])
def tasksid(id = None):
  if request.method == "DELETE":
        deleted_tasks = Tasks.query.filter_by(id = id).first()
        if deleted_tasks is not None:
            db.session.delete(deleted_tasks)
            db.session.commit() 
            return jsonify(deleted_tasks.serialize_username())
        
        db.session.remove(deleted_tasks)
        db.session.commit()
        return jsonify(deleted_tasks.serialize()), 200


if __name__ == "__main__":
    app.run(host ="localhost", port = 1080)
