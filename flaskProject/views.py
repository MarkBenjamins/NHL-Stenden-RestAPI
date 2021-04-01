from flask import Blueprint, render_template, request, flash, jsonify

views = Blueprint('views', __name__)


@views.route('/views')
def vieuws():
    return "h1>Hallo</h1>"
