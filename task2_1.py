from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f"Customer('{self.name}' '{self.surname}' - '{self.email}')"


class Pc(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cpu = db.Column(db.String(100), nullable=False)
    ram = db.Column(db.String(10), nullable=False)
    ssd = db.Column(db.String(10), nullable=False)
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"PC('{self.cpu}', '{self.ram}', '{self.ssd}' - '{self.price}')"


class Deal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer = db.relationship('Customer', backref='deals', lazy=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    pc = db.relationship('Pc', backref='deals', lazy=True)
    pc_id = db.Column(db.Integer, db.ForeignKey('pc.id'), nullable=False) 
    price = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Deal('{self.customer_id}' - '{self.pc_id}')"


class CustomerApi(Resource):
    def get(self, customer_id):
        customer = Customer.query.get(customer_id)
        if customer is None:
            return jsonify({'status': 'Failed'})
        deal_list = {}
        for deal in customer.deals:
            deal_list[deal.id] = {'pc_id': deal.pc_id, 'price': deal.price}
        return jsonify(deal_list)


    def post(self):
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        customer = Customer(name=name, surname=surname, email=email)
        db.session.add(customer)
        db.session.commit()
        return jsonify({
            'customer_id': customer.id,
            'name': customer.name,
            'surname': customer.surname,
            'email': customer.email
        })

    def delete(self, customer_id):
        # customer_id = request.form['customer_id']
        customer = Customer.query.get(customer_id)
        if customer is None:
            return jsonify({'status': 'Failed'})
        deleted_customer = jsonify({
            'status': 'Success',
            'customer_id': customer.id,
            'name': customer.name,
            'surname': customer.surname,
            'email': customer.email
        })
        db.session.delete(customer)
        db.session.commit()
        return deleted_customer


class PCApi(Resource):
    def get(self, pc_id):
        pc = Pc.query.get(pc_id)
        if pc is None:
            return jsonify({'status': "Failed"})
        customer_list = {}
        for deal in pc.deals:
           customer = Customer.query.get(deal.customer_id)
           customer_list[customer.id] = {'name': customer.name, 'surname': customer.surname, 'email': customer.email}
        return jsonify(customer_list)

    def post(self):
        cpu = request.form['cpu']
        ram = request.form['ram']
        ssd = request.form['ssd']
        price = request.form['price']
        pc = Pc(cpu=cpu, ram=ram, ssd=ssd, price=price)
        db.session.add(pc)
        db.session.commit()
        return jsonify({
            'pc_id': pc.id,
            'cpu': pc.cpu,
            'ram': pc.ram,
            'ssd': pc.ssd,
            'price': pc.price
        })
    
    def delete(self, pc_id):
        # pc_id = request.form['pc_id']
        pc = Pc.query.get(pc_id)
        if pc is None:
            return jsonify({'status': 'Failed'})
        deleted_pc = jsonify({
            'status': 'Success',
            'pc_id': pc.id,
            'cpu': pc.cpu,
            'ram': pc.ram,
            'ssd': pc.ssd,
            'pc_price': pc.price
            })
        db.session.delete(pc)
        db.session.commit()
        return deleted_pc


class DealApi(Resource):
    def post(self):
        customer_id = request.form['customer_id']
        pc_id = request.form['pc_id']
        price = request.form['price']
        deal = Deal(customer=Customer.query.get(customer_id), customer_id=customer_id, pc=Pc.query.get(pc_id), pc_id=pc_id, price=price)
        db.session.add(deal)
        db.session.commit()
        return jsonify({
            'customer_id': deal.customer_id,
            'pc_id': deal.pc_id,
            'price': deal.price
        })


class BestBuyer(Resource):
    def get(self):
        customers = Customer.query.all()
        prices = {}
        for customer in customers:
            prices[customer.id] = 0
            for deal in customer.deals:
                prices[customer.id] += deal.price
        max_key = max(prices, key=prices.get)
        customer = Customer.query.get(max_key)
        return jsonify({
            'customer_id': max_key,
            'name': customer.name,
            'surname': customer.surname,
            'Money spent': prices[max_key]
        })
        

api.add_resource(CustomerApi, '/customer', '/customer/<int:customer_id>')
api.add_resource(PCApi, '/pc', '/pc/<int:pc_id>')
api.add_resource(DealApi, '/deal')
api.add_resource(BestBuyer, '/best_customer')

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
