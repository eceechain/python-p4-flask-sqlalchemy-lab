#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

def format_attributes(obj):
    return [f"<li>{attr}: {getattr(obj, attr)}</li>" for attr in obj.__dict__ if not callable(getattr(obj, attr)) and not attr.startswith("_")]

def create_response(obj_type, attributes):
    return make_response(f"<h2>{obj_type}</h2><ul>{''.join(attributes)}</ul>", 200)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get(id)
    if animal:
        response_body = format_attributes(animal)
        return create_response("Animal", response_body)
    else:
        return make_response("Animal not found", 404)

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get(id)
    if zookeeper:
        response_body = format_attributes(zookeeper)
        return create_response("Zookeeper", response_body)
    else:
        return make_response("Zookeeper not found", 404)

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    enclosure = Enclosure.query.get(id)
    if enclosure:
        response_body = format_attributes(enclosure)
        return create_response("Enclosure", response_body)
    else:
        return make_response("Enclosure not found", 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)
