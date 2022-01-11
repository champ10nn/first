# curl 'http://localhost:5000/api/pcs' -d '{"cpu": "i5", "ssd": "128", "ram": "4", "price": 700}' -X POST -v
# curl 'http://localhost:5000/api/pcs' -d '{"cpu": "i7", "ssd": "128", "ram": "8", "price": 1000}' -X POST -v
# requests.post('http://localhost:5000/api/pcs', data='{"cpu": "i5", "ssd": "128", "ram": "4", "price": 700}').json()


# curl 'http://localhost:5000/api/customers' -d '{"name":"Turgut", "surname": "Agha", "email": "t@t.com"}' -X POST -v
# curl 'http://localhost:5000/api/customers' -d '{"name":"Murad", "surname": "Sharif", "email": "m@m.com"}' -X POST -v
# requests.post('http://localhost:5000/api/customers', data='{"name":"Murad", "surname": "Sharif", "email": "m@m.com"}').json()


# curl 'http://localhost:5000/api/deals' -d '{"pc_id": 1, "cs_id": 1}' -X POST -v
# curl 'http://localhost:5000/api/deals' -d '{"pc_id": 2, "cs_id": 1}' -X POST -v
# requests.post('http://localhost:5000/api/deals', data='{"pc_id": 2, "cs_id": 1}').json()

# curl 'http://localhost:5000/api/customers/1' -X GET -v
# requests.get('http://localhost:5000/api/customers/1').json()

# curl 'http://localhost:5000/api/pcs/1' -X GET -v
# requests.get('http://localhost:5000/api/pcs/4').json()

# curl 'http://localhost:5000/api/bestbuyer' -X GET -v
# requests.get('http://localhost:5000/api/bestbuyer').json()