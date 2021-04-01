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

employees = [
    {"employeeID": 100, "firstName": "Pieter", "middleInitial": "", "lastName": "Post"},
    {"employeeID": 101, "firstName": "Jannie", "middleInitial": "", "lastName": "Post"},
    {"employeeID": 102, "firstName": "Jannes", "middleInitial": "", "lastName": "Post"}
]

customers = [
    {"customerID": 10, "firstName": "Karel", "middleInitial": "", "lastName": "Bos"},
    {"customerID": 11, "firstName": "Jan", "middleInitial": "", "lastName": "Klassen"},
    {"customerID": 12, "firstName": "Bert", "middleInitial": "en", "lastName": "Ernie"}
]
sales = [
    {"salesID": 21, "salePersonalID": 211, "customerID": 201, "productID": 31, "quantity": 75},
    {"salesID": 22, "salesPersonalID": 206, "customerID": 303, "productID": 6, "quantity": 5},
    {"salesID": 23, "salesPersonalID": 207, "customerID": 303, "productID": 8, "quantity": 5}
]


############################ Homepage ################################
# The home page
@app.route('/', methods=['GET'])
def home():
    return render_template("home.html")


############################ Product ################################
# GET the products
@app.route('/products', methods=['GET'])
def getProducts():
    return jsonify(products)  # Products to JSON file


# GET the product with ID
@app.route('/product', methods=["GET", "POST"])
def getProductWithID():
    if request.method == "POST":
        # todo dont use hardcode validate
        productInput = request.form.get('productInput')
        if int(productInput) > 0 and int(productInput) < 4:
            for product in products:
                if product["productID"] == int(productInput):
                    pro = product["productID"]
                    name = product["name"]
                    price = product["price"]
                    output = render_template("product.html",
                                             productID=pro,
                                             name=name,
                                             price=price,
                                             result="yes")
                    return output
        else:
            output = render_template("product.html", noresult="Geen resultaat")
            return output

    else:
        output = render_template("product.html")
        return output

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


############################ Employees ################################
# GET the employees
@app.route('/employees', methods=['GET'])
def getEmployees():  # Lijst van de employees
    return jsonify(employees)  # maakt een JSON van employees


# GET the employee with ID
@app.route('/employee', methods=["GET", "POST"])
def getEmplyeeWithID():
    if request.method == "POST":
        employeeInput = request.form.get('employeeInput')
        #todo dont use hardcode validate
        if int(employeeInput) > 99 and int(employeeInput) < 103:
            for employee in employees:
                if employee["employeeID"] == int(employeeInput):
                    employeeID = employee["employeeID"]
                    fname = employee["firstName"]
                    mname = employee["middleInitial"]
                    lname = employee["lastName"]
                    output = render_template("employee.html",
                                             employeeID=employeeID,
                                             fname=fname,
                                             mname=mname,
                                             lname=lname,
                                             result="yes")
                    return output
        else:
            output = render_template("employee.html", noresult="Geen resultaat")
            return output

    else:
        output = render_template("employee.html")
        return output


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


# GET the customer with ID
@app.route('/customer', methods=["GET", "POST"])
def getCustomerWithID():
    if request.method == "POST":
        customerInput = request.form.get('customerInput')
        #todo dont use hardcode validate
        if int(customerInput) > 9 and int(customerInput) < 13:
            for customer in customers:
                if customer["customerID"] == int(customerInput):
                    customerID = customer["customerID"]
                    fname = customer["firstName"]
                    mname = customer["middleInitial"]
                    lname = customer["lastName"]
                    output = render_template("customer.html",
                                             customerID=customerID,
                                             fname=fname,
                                             mname=mname,
                                             lname=lname,
                                             result="yes")
                    return output
        else:
            output = render_template("customer.html", noresult="Geen resultaat")
            return output

    else:
        output = render_template("customer.html")
        return output


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

############################ Sale #####################################
# GET the sale
@app.route('/sales', methods=['GET'])
def getSales():  # Lijst van de sales
    return jsonify(sales)  # maakt een JSON van sales
    # todo fix the sales dataset

###
#todo make it work
# GET the sale with ID
@app.route('/sale', methods=["GET", "POST"])
def getSaleWithID():
    if request.method == "POST":
        saleInput = request.form.get('saleInput')
        #todo dont use hardcode validate
        if int(saleInput) > 20 and int(saleInput) < 24:
            for sale in sales:
                if sale["salesID"] == int(saleInput):
                    salesID = sale["salesID"]
                    spID = sale["salesPersonalID"]
                    cid = sale["customerID"]
                    pid = sale["productID"]
                    qua = sale["quantity"]
                    output = render_template("sale.html",
                                             salesID=salesID,
                                             spID=spID,
                                             cid=cid,
                                             pid=pid,
                                             qua=qua,
                                             result="yes")
                    return output
        else:
            output = render_template("sale.html", noresult="Geen resultaat")
            return output

    else:
        output = render_template("sale.html")
        return output

####
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


############################ TEST CODE #######################################



# Debug function enabled
if __name__ == "__main__":
    app.run(debug=True)
