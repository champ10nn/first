from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///skyway.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)


travels = db.Table('travels', db.Column('flight_id', db.Integer, db.ForeignKey('flights.id'), primary_key=True),
        db.Column('passenger_id', db.Integer, db.ForeignKey('passengers.id'), primary_key=True))


class FlightModel(db.Model):
    __tablename__ = 'flights'
    id = db.Column(db.Integer, primary_key=True)
    airplane = db.Column(db.Integer, db.ForeignKey('airplanes.id'), nullable=False)
    arrival_city = db.Column(db.String(50), nullable=False)
    departure_city = db.Column(db.String(50), nullable=False)
    arrival_datetime = db.Column(db.String(100), nullable=False)
    departure_datetime = db.Column(db.String(100), nullable=False)
    pass_list = db.Column(db.Text, nullable=False)
    passengers = db.relationship('PassengerModel', secondary=travels, lazy='subquery', backref=db.backref('flights', lazy=True))


class AirplaneModel(db.Model):
    __tablename__ = 'airplanes'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    max_pass = db.Column(db.Integer, nullable=False)


class PassengerModel(db.Model):
    __tablename__ = 'passengers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    phone = db.Column(db.String(100), nullable=False, unique=True)


class Passenger(Resource):
    def get(self, passenger_id):
        passenger = PassengerModel.query.get(passenger_id)
        if passenger is None:
            return jsonify({'status': "Failed"})
        flight_list = {}
        for flight in passenger.flights:
            flight_list[flight.id] = {'departure_datetime': flight.departure_datetime, 'arrival_datetime': flight.arrival_datetime}
        return jsonify(flight_list)

    def post(self):
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        phone = request.form['phone']
        passenger = PassengerModel(name=name, surname=surname, email=email, phone=phone)
        db.session.add(passenger)
        db.session.commit()
        return jsonify({
            'id': passenger.id,
            'name': passenger.name,
            'surname': passenger.surname,
            'email': passenger.email,
            'phone': passenger.phone,
        })

    def delete(self, passenger_id):
        passenger = PassengerModel.query.get(passenger_id)
        if passenger is None:
            return jsonify({'status': 'Failed'})
        deleted_passenger = jsonify({
            'id': passenger.id,
            'name': passenger.name,
            'surname': passenger.surname
        })
        db.session.delete(passenger)
        db.session.commit()
        return deleted_passenger


class Flight(Resource):
    def post(self):
        airplane = request.form['airplane']
        arrival_city = request.form['arrival_city']
        departure_city = request.form['departure_city']
        arrival_datetime = request.form['arrival_datetime']
        departure_datetime = request.form['departure_datetime']
        pass_list = request.form['pass_list']
        flight = FlightModel(airplane=airplane, arrival_city=arrival_city, departure_city=departure_city, arrival_datetime=arrival_datetime,
                departure_datetime=departure_datetime, pass_list=pass_list)
        pass_list = pass_list.split(',')
        for passenger in pass_list:
            flight.passengers.append(PassengerModel.query.get(passenger))
        db.session.add(flight)
        db.session.commit()
        return jsonify({
            'id': flight.id,
            'airplane': flight.airplane,
            'pass_list': flight.pass_list
        })

 
class Airplane(Resource):
    def post(self):
        title = request.form['title']
        max_pass = request.form['max_pass']
        airplane = AirplaneModel(title=title, max_pass=max_pass)
        db.session.add(airplane)
        db.session.commit()
        return jsonify({
            'id': airplane.id,
            'title': airplane.title,
            'max_pass': airplane.max_pass
        })

    def delete(self, airplane_id):
        airplane = AirplaneModel.query.get(airplane_id)
        if airplane is None:
            return jsonify({'status': 'Failed'})
        deleted_airplane = jsonify({
            'status': "success",
            'airplane_title': airplane.title,
            'max_passengers': airplane.max_pass
        })
        db.session.delete(airplane)
        db.session.commit()
        return deleted_airplane


class FlightOperations(Resource):
    def post(self, flight_id):
        passenger_id = request.form['passenger_id']
        passenger = PassengerModel.query.get(passenger_id)
        flight = FlightModel.query.get(flight_id)
        if passenger is None or flight is None:
            return jsonify({'status': 'Failed'})
        if passenger in flight.passengers:
            return jsonify({'message': 'Already in flight'})
        flight.passengers.append(passenger)
        db.session.commit()
        pass_list = []
        for p in flight.passengers:
            pass_list.append(p.id)
        return jsonify({
            'flight_id': flight.id,
            'passenger_list': pass_list
        })

    def get(self, flight_id):
        flight = FlightModel.query.get(flight_id)
        if flight is None:
            return jsonify({'status':"Failed"})
        pass_list={}
        for p in flight.passengers:
            pass_list[p.id] = {'name': p.name, 'surname': p.surname, 'email': p.email, 'phone': p.phone}
        return jsonify(pass_list)



def main():
    api.add_resource(Flight, '/flight')
    api.add_resource(Airplane, '/airplane', '/airplane/<int:airplane_id>')
    api.add_resource(Passenger, '/passenger', '/passenger/<int:passenger_id>')
    api.add_resource(FlightOperations, '/flight/<int:flight_id>')

if __name__ == "__main__":
    db.create_all()
    main()
    app.run(debug=True)
