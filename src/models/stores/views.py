from flask import Blueprint, render_template

store_blueprint =  Blueprint('stores', __name__)

@store_blueprint.route('/')
def index():
    stores = []
    return render_template('stores/store_index.html')


@store_blueprint.route('/store/<string:name>')
def store_page():
    pass

@store_blueprint.route('/new', methods=['GET', 'POST'])
def create_store():
    return "This is the store creation page"