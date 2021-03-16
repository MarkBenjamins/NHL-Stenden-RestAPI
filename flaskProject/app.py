from flask import Flask, redirect, url_for, render_template, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Debug function enabled
# if __name__ == "__main__":
#    app.run(debug=True)

# The home page
@app.route('/')
def home():
    return render_template("Home.html")

# The product search page
@app.route('/Product', methods=['POST', 'GET'])
def Products():
    if request.method == "POST":
        Product = request.form["FormProductID"]
        return redirect(url_for("Product", productID=Product))
    else:
        return render_template("ProductSalesPage.html")

# Product search page input
@app.route("/<productID>")
def Product(productID):
    #TODO dit werkt niet het geeft het {ProductID} weer i.p.v. de input maar in de url staat de input wel
    return "<h1>{productID}</h1>"


@app.route('/Customers', methods=['POST', 'GET'])
def Customers():
    return "<h1> Customers page </1>"

if __name__ == '__main__':
    app.run()


