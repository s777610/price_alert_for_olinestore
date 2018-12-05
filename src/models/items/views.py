from flask import Blueprint

item_blueprint = Blueprint('items', __name__)

@item_blueprint.route('/<string:name>')
def item_page(name):
    pass


