from flask import Flask, render_template, request, jsonify, Response, abort, Blueprint
from flaskProject import create_app

import xmltodict
import uuid
import validator
import json

auth = Blueprint('auth', __name__)

app = Flask(__name__)
app1 = create_app()

# if __name__ == '__main__':
#   app.run()

# Data
products = [
    {"productID": 1, "name": "cat food", "price": 1.25},
    {"productID": 2, "name": "dog food", "price": 5.35},
    {"productID": 3, "name": "guinea pig food", "price": 12.00}
]

sales = [
    {"salesID": 1, "salesPersonalID": 200, "customerID": 301, "productID": 1, "quantity": 5}
]

employees = [
    {"EmployeeID": 100, "firstName": "Mark", "middleInitial": "", "lastName": "Benjamins"},
    {"EmployeeID": 101, "firstName": "Niels", "middleInitial": "", "lastName": "Benjamins"}
]

customers = [
    {"customerID": 10, "firstName": "karel", "middleInitial": "", "lastName": "Bos"}
]


############################ Homepage ################################
# The home page
@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


############################ Product ################################
# GET the product
@app.route('/products', methods=['GET'])
def getProducts():
    return jsonify(products)  # Products to JSON file


###
# todo fix this man
# GET the product of the ID
@app.route('/product', methods=["GET", "POST"])
def getProductsWithID():
    if request.method == "POST":
        # user input number
        productInput = request.form.get('productInput')
        if int(productInput) > 0 and int(productInput) < 4:
            for product in products:
                if product["productID"] == int(productInput):
                    a = render_template("product.html", productID=product["productID"], name=product["name"], price=product["price"])
                    return a
        else:
            a = render_template("product.html", productID="Geen resultaat")
            return a

    else:
        a = render_template("product.html")
        return a


###

# todo validatie goed maken dat hij wel door laat
# POST the product
@app.route('/products', methods=['POST'])
def postProducts():
    content = request.headers.get('Content-Type')

    # als het XML is
    if content == "application/xml":
        xmlData = xmltodict.parse(request.data)
        is_valid = validator.is_valid_xml(xmlData)
        if is_valid:
            xmlData["productID"] = uuid.uuid4()
            products.append(xmlData)
            return xmlData
        else:
            abort(400)  # error code 400

    # als het JSON is
    else:
        if not request.json:
            abort(400)  # error code 400
        else:
            jsonData = request.json
            is_valid = validator.is_valid_json(json.dumps(jsonData))
            if is_valid:
                jsonData["productID"] = uuid.uuid4()
                products.append(jsonData)
                return jsonData
            else:
                abort(400)  # error code 400


# PUT the product
@app.route('/products/<productID>', methods=['PUT'])
def putProducts():
    content = request.headers.get('Content-Type')
    id = request.view_args['productID']

    # todo afmaken
    for product in products:
        if product["productID"] == id:

            # als het XML is
            if content == "application/xml":
                xmlData = xmltodict.parse(request.data)
                xmlData["productID"] = id  # zet het ID vast
                index = products.index(product)  # bepaald de rij die geupdate word
                products[index] = xmlData
                return xmlData

            # als het JSON is
            # todo validatie
            else:
                if not request.json:
                    abort(400)  # error als foutmelding
                jsonData = request.json
                jsonData["productID"] = uuid.uuid4()
                products.append(jsonData)
                return jsonData


# DELETE the product
@app.route('/products/<id>', methods=['DELETE'])
def delProducts(id):
    response = Response()
    for product in products:
        if product["id"] == int(id):
            products.remove(product)
            response.status_code = 200
        else:
            response.status_code = 404
    return response


############################ Sale #####################################
# GET the sale
@app.route('/sales', methods=['GET'])
def getSales():  # Lijst van de sales
    return jsonify(sales)  # maakt een JSON van sales
    # todo fix the sales dataset


# POST the sale
@app.route('/sales', methods=['POST'])
def postSales():
    content = request.headers.get('Content-Type')

    # als het XML is
    if content == "application/xml":
        xmlData = xmltodict.parse(request.data)
        xmlData["id"] = uuid.uuid4()
        products.append(xmlData)
        return xmlData

    # als het JSON is
    else:
        if not request.json:
            abort(400)  # error als foutmelding
        jsonData = request.json
        jsonData["id"] = uuid.uuid4()
        products.append(jsonData)
        return jsonData


# PUT the sale #todo afmaken
# @app.route('/sales/<id>', methods=['PUT'])
# def putSales():
#     content = request.headers.get('Content-Type')
#     id = request.view_args['id']


# DELETE the sale
@app.route('/sales/<id>', methods=['DELETE'])
def delSales(id):
    response = Response()
    for sale in sales:
        if sale["id"] == int(id):
            sales.remove(sale)
            response.status_code = 200
        else:
            response.status_code = 404
    return response


############################ Employees ################################
# GET the employee
@app.route('/employees', methods=['GET'])
def getEmployees():  # Lijst van de employees
    return jsonify(employees)  # maakt een JSON van employees


# POST the employee
@app.route('/employees', methods=['POST'])
def postEmployees():
    content = request.headers.get('Content-Type')

    # als het XML is
    if content == "application/xml":
        xmlData = xmltodict.parse(request.data)
        xmlData["id"] = uuid.uuid4()
        products.append(xmlData)
        return xmlData

    # als het JSON is
    else:
        if not request.json:
            abort(400)  # error als foutmelding
        jsonData = request.json
        jsonData["id"] = uuid.uuid4()
        products.append(jsonData)
        return jsonData


# DELETE the employee
@app.route('/employees/<id>', methods=['DELETE'])
def delEmployees(id):
    response = Response()
    for employee in employees:
        if employee["id"] == int(id):
            employees.remove(employee)
            response.status_code = 200
        else:
            response.status_code = 404
    return response


############################ Customers ################################
# GET the customer
@app.route('/customers', methods=['GET'])
def getCustomers():  # Lijst van de customers
    return jsonify(customers)  # maakt een JSON van customers


# POST the customer
@app.route('/customers', methods=['POST'])
def postCustomers():
    content = request.headers.get('Content-Type')

    # als het XML is
    if content == "application/xml":
        xmlData = xmltodict.parse(request.data)
        xmlData["id"] = uuid.uuid4()
        products.append(xmlData)
        return xmlData

    # als het JSON is
    else:
        if not request.json:
            abort(400)  # error als foutmelding
        jsonData = request.json
        jsonData["id"] = uuid.uuid4()
        products.append(jsonData)
        return jsonData


# DELETE the customers
@app.route('/customers/<id>', methods=['DELETE'])
def delcustomers(id):
    response = Response()
    for customer in customers:
        if customer["id"] == int(id):
            customers.remove(customer)
            response.status_code = 200
        else:
            response.status_code = 404
    return response


############################ TEST CODE #######################################

@app.route('/login', methods=['GET', 'POST'])
# @auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # todo input validatie
        email = request.form.get('email')
        ww = request.form.get('password')

        # klik zoek er is mark
        e = render_template("login.html", test=email + ww)
    else:
        # start geen mark
        e = render_template("login.html")
    return e


# Debug function enabled
if __name__ == "__main__":
    app.run(debug=True)
