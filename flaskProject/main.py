from flask import Flask, render_template, request, jsonify, Response, abort

import xmltodict
import uuid
import validator
import json

app = Flask(__name__)

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
    {"customerID": 11, "firstName": "Jan", "middleInitial": "", "lastName": "Pieter"},
    {"customerID": 12, "firstName": "Bert", "middleInitial": "en", "lastName": "Ernie"}
]
sales = [
    {"salesID": 21, "salesPersonalID": 211, "customerID": 201, "productID": 31, "quantity": 75},
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
    return jsonify(products)


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
            output = render_template("product.html", noresult="No result")
            return output

    else:
        output = render_template("product.html")
        return output


# POST the product
# todo validation
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
            abort(400)

    # als het JSON is
    else:
        if not request.json:
            abort(400)
        else:
            jsonData = request.json
            is_valid = validator.is_valid_json(json.dumps(jsonData))
            if is_valid:
                jsonData["productID"] = uuid.uuid4()
                products.append(jsonData)
                return jsonData
            else:
                abort(400)


# PUT the product
# todo validation
@app.route('/products/<productID>', methods=['PUT'])
def putProducts():
    content = request.headers.get('Content-Type')
    pid = request.view_args['productID']

    for product in products:
        if product["productID"] == pid:

            # als het XML is
            if content == "application/xml":
                xmlData = xmltodict.parse(request.data)
                xmlData["productID"] = pid
                index = products.index(product)
                products[index] = xmlData
                return xmlData

            # als het JSON is
            else:
                if not request.json:
                    abort(400)
                jsonData = request.json
                jsonData["productID"] = uuid.uuid4()
                products.append(jsonData)
                return jsonData


# DELETE the product
@app.route('/products/<pid>', methods=['DELETE'])
def delProducts(pid):
    response = Response()
    for product in products:
        if product["productID"] == int(pid):
            print(pid + " Has been deleted")
            products.remove(product)
            response.status_code = 200
        else:
            print(pid + " Has not been deleted")
            response.status_code = 404
        return response


############################ Employees ################################
# GET the employees
@app.route('/employees', methods=['GET'])
def getEmployees():
    return jsonify(employees)


# GET the employee with ID
@app.route('/employee', methods=["GET", "POST"])
def getEmployeeWithID():
    if request.method == "POST":
        employeeInput = request.form.get('employeeInput')
        # todo dont use hardcode validate
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
            output = render_template("employee.html", noresult="No result")
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
        xmlData["employeeID"] = uuid.uuid4()
        products.append(xmlData)
        return xmlData

    # als het JSON is
    else:
        if not request.json:
            abort(400)
        jsonData = request.json
        jsonData["employeeID"] = uuid.uuid4()
        products.append(jsonData)
        return jsonData


# PUT the employee
# todo validation
@app.route('/employees/<employeeID>', methods=['PUT'])
def putEmployees():
    content = request.headers.get('Content-Type')
    eid = request.view_args['employeeID']

    for employee in employees:
        if employee["employeeID"] == eid:

            # als het XML is
            if content == "application/xml":
                xmlData = xmltodict.parse(request.data)
                xmlData["employeeID"] = eid
                index = employees.index(employee)
                employees[index] = xmlData
                return xmlData

            # als het JSON is
            else:
                if not request.json:
                    abort(400)
                jsonData = request.json
                jsonData["employeeID"] = uuid.uuid4()
                employees.append(jsonData)
                return jsonData


# DELETE the employee
@app.route('/employees/<employeeID>', methods=['DELETE'])
def delEmployees(employeeID):
    response = Response()
    for employee in employees:
        if employee["employeeID"] == int(employeeID):
            print(employeeID + " Has been deleted")
            employees.remove(employee)
            response.status_code = 200
        else:
            print(employeeID + " Has not been deleted")
            response.status_code = 404
        return response


############################ Customers ################################
# GET the customer
@app.route('/customers', methods=['GET'])
def getCustomers():
    return jsonify(customers)


# GET the customer with ID
@app.route('/customer', methods=["GET", "POST"])
def getCustomerWithID():
    if request.method == "POST":
        customerInput = request.form.get('customerInput')
        # todo dont use hardcode validate
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
            output = render_template("customer.html", noresult="No result")
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
        xmlData["customerID"] = uuid.uuid4()
        products.append(xmlData)
        return xmlData

    # als het JSON is
    else:
        if not request.json:
            abort(400)
        jsonData = request.json
        jsonData["customerID"] = uuid.uuid4()
        products.append(jsonData)
        return jsonData


# PUT the customer
# todo validation
@app.route('/customers/<customerID>', methods=['PUT'])
def putCustomers():
    content = request.headers.get('Content-Type')
    cid = request.view_args['customerID']

    for customer in customers:
        if customer["customerID"] == cid:

            # als het XML is
            if content == "application/xml":
                xmlData = xmltodict.parse(request.data)
                xmlData["customerID"] = cid
                index = customers.index(customer)
                customers[index] = xmlData
                return xmlData

            # als het JSON is
            else:
                if not request.json:
                    abort(400)
                jsonData = request.json
                jsonData["customerID"] = uuid.uuid4()
                customers.append(jsonData)
                return jsonData


# DELETE the customers
@app.route('/customers/<customerID>', methods=['DELETE'])
def delCustomers(customerID):
    response = Response()
    for customer in customers:
        if customer["customerID"] == int(customerID):
            print(customerID + " Has been deleted")
            customers.remove(customer)
            response.status_code = 200
        else:
            print(customerID + " Has not been deleted")
            response.status_code = 404
        return response


############################ Sale #####################################
# GET the sale
@app.route('/sales', methods=['GET'])
def getSales():
    return jsonify(sales)


# GET the sale with ID
@app.route('/sale', methods=["GET", "POST"])
def getSaleWithID():
    if request.method == "POST":
        saleInput = request.form.get('saleInput')
        # todo dont use hardcode validate
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
            output = render_template("sale.html", noresult="No result")
            return output

    else:
        output = render_template("sale.html")
        return output


# PUT the sale
# todo validation
@app.route('/sales/<saleID>', methods=['PUT'])
def putSales():
    content = request.headers.get('Content-Type')
    cid = request.view_args['saleID']

    for sale in sales:
        if sale["saleID"] == cid:

            # als het XML is
            if content == "application/xml":
                xmlData = xmltodict.parse(request.data)
                xmlData["saleID"] = cid
                index = customers.index(sale)
                sale[index] = xmlData
                return xmlData

            # als het JSON is
            else:
                if not request.json:
                    abort(400)
                jsonData = request.json
                jsonData["saleID"] = uuid.uuid4()
                sale.append(jsonData)
                return jsonData


# POST the sale
@app.route('/sales', methods=['POST'])
def postSales():
    content = request.headers.get('Content-Type')

    # als het XML is
    if content == "application/xml":
        xmlData = xmltodict.parse(request.data)
        xmlData["salesID"] = uuid.uuid4()
        products.append(xmlData)
        return xmlData

    # als het JSON is
    else:
        if not request.json:
            abort(400)
        jsonData = request.json
        jsonData["salesID"] = uuid.uuid4()
        products.append(jsonData)
        return jsonData


# DELETE the sale
@app.route('/sales/<salesID>', methods=['DELETE'])
def delSales(salesID):
    response = Response()
    for sale in sales:
        if sale["salesID"] == int(salesID):
            print(salesID + " Has been deleted")
            sales.remove(sale)
            response.status_code = 200
        else:
            print(salesID + " Has not been deleted")
            response.status_code = 404
        return response


# Debug function enabled
if __name__ == "__main__":
    app.run(debug=True)