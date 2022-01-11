from math import fabs
from flask import Flask, request, jsonify
from flask.scaffold import F
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


## version 1

class PCModel(db.Model):
    __tablename__ = 'pcs'
    id = db.Column(db.Integer, primary_key=True)

class CustomerModel(db.Model):
    __tablename__ = "customers"
    id = db.Column(db.Integer, primary_key=True)

class DealModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    pc_id = db.Column(db.Integer, db.ForeignKey('pcs.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    pc = db.relationship('PCModel', backref='deals', lazy="True")
    customer = db.relationship('CustomerModel', backref='deals', lazy="True")
    
    
## version 2

travels = db.Table('travels',
    db.Column('flight_id', db.Integer, db.ForeignKey('flights.id') ,primary_key=True),
    db.Column('passenger_id', db.Integer, db.ForeignKey('passengers.id'), primary_key=True)
)

class AirplaneModel(db.Model):
    __tablename__ = "airplanes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    max_pass = db.Column(db.Integer, nullable=False)

class PassengerModel(db.Model):
    __tablename__ = "passengers"
    id = db.Column(db.Integer, primary_key=True)


class FlightModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    airplane_id = db.Column(db.Integer, db.ForeignKey("airplanes.id"), nullable=False)
    pass_list = db.Column(db.Text, nullable=False)
    passengers = db.relationship('PassengerModel', secondary=travels, lazy='subquery', backref=db.backref('flights', lazy=True))




class PC(Resource):
    def get(self, id):
        pass

    def put(self, id):
        pass
    
    def delete(self, id):
        pass
    
    def post(self):
        pass

def main():
    api.add_resource(PC, '/api/pcs', '/api/pcs/<int:id>')

if __name__ == "__main__":
    db.create_all()
    main()
    app.run(debug=True)