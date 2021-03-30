from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_restful import Api, Resource, abort

import xmltodict
import uuid

#
app = Flask(__name__)
api = Api(app)


#Data
products = [
            {"name": 'kattenvoer', "price": 1.25},
            {"name": 'hondenvoer', "price": 1.25}
           ]

#todo vind uit hoe je de ids pakt van de andere setes
sales =    [
#            {"productID": product<id>, "productID": product<id>,"quantity": 5}
           ]

employees = [
            {"firstName": "Mark", "middleInitial": "", "lastName": "Benjamins"},
            {"firstName": "Niels", "middleInitial": "", "lastName": "Benjamins"}
           ]

customers = [
            {"firstName": "karel", "middleInitial": "", "lastName": "Bos"}
           ]



# class Sale(Resource):
#     def get(self, sale):
#         return sales[sale]
#
#     def post(self):
#         return {"data": "posted"}
#
# api.add_resource(Sale, "/sale/<string:sale>")


# The home page
@app.route('/')
def home():
    return render_template("home.html")

############################ Product ################################

# GET the product
@app.route('/products', methods=['GET'])
def getProducts(): # Lijst van de producten
    return jsonify(products) # maakt een JSON van producten

# POST the product
@app.route('/products', methods=['POST'])
def postProducts():
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

# PUT the product
@app.route('/products/<id>', methods=['PUT'])
def putProducts():
    content = request.headers.get('Content-Type')
    id = request.view_args['id']

#todo
    for product in products:
        if product["id"] == id:

            # als het XML is
            if content == "application/xml":
                xmlData = xmltodict.parse(request.data)
                xmlData["id"] = id # zet het ID vast
                index = products.index(product) # bepaald de rijd die geupdate word
                products[index] = xmlData
                return xmlData

            # als het JSON is
# todo validatie
            else:
                if not request.json:
                    abort(400)  # error als foutmelding
                jsonData = request.json
                jsonData["id"] = uuid.uuid4()
                products.append(jsonData)
                return jsonData

############################ Sale #####################################
# GET the sale
@app.route('/sales', methods=['GET'])
def getSales(): # Lijst van de sales
    return jsonify(sales) # maakt een JSON van sales

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

############################ Employees ################################
# GET the employee
@app.route('/employees', methods=['GET'])
def getEmployees(): # Lijst van de employees
    return jsonify(employees) # maakt een JSON van employees
#todo make een JSON met de data van employees

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

############################ Customers ################################
# GET the customer
@app.route('/customers', methods=['GET'])
def getCustomers(): # Lijst van de customers
    return jsonify(customers) # maakt een JSON van customers
#todo make een JSON met de data van customers

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


#######################################################################
# Debug function enabled
if __name__ == "__main__":
    app.run(debug=True)


#if __name__ == '__main__':
 #   app.run()


