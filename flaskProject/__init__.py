from flask import Flask, render_template, request, jsonify, Response, abort


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "abc"

    from .views import views

    app.register_blueprint(views, url_prefix='/')

    return app
