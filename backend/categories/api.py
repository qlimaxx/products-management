import os

from functools import wraps
from flask import Flask, request, jsonify
from mongoengine import connect
from mongoengine.errors import ValidationError, NotUniqueError

from .models import Category


app = Flask(__name__)
app.config['API_KEY'] = os.environ.get('API_KEY')
app.config['MONGO_URI'] = os.environ.get(
    'MONGO_URI', default='mongodb://localhost')

connect('db', host=app.config['MONGO_URI'])


def require_auth(func):
    @wraps(func)
    def auth(*args, **kwargs):
        if request.headers.get('X-API-Key') is None:
            return jsonify({'details': 'X-API-Key is missing'}), 403
        elif request.headers.get('X-API-Key') != app.config['API_KEY']:
            return jsonify({'details': 'Invalid X-API-Key'}), 403
        return func(*args, **kwargs)
    return auth


def handle_error(func):
    @wraps(func)
    def error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ValueError, ValidationError, NotUniqueError) as ex:
            return jsonify({'details': str(ex)}), 400
        except Category.DoesNotExist as ex:
            return jsonify({'details': str(ex)}), 404
        except Exception:
            return '', 400
    return error


@app.route('/', methods=['GET'])
@require_auth
@handle_error
def get_categories():
    data = []
    for category in Category.objects.all():
        data.append(category.to_dict())
    return jsonify(data)


@app.route('/', methods=['POST'])
@require_auth
@handle_error
def create_category():
    data = request.get_json()
    category = Category(name=data.get('name'))
    category.save()
    return jsonify(category.to_dict())


@app.route('/<category_id>', methods=['GET'])
@require_auth
@handle_error
def get_category(category_id):
    category = Category.objects.get(uuid=category_id)
    return jsonify(category.to_dict())


@app.route('/<category_id>', methods=['PUT'])
@require_auth
@handle_error
def update_category(category_id):
    data = request.get_json()
    category = Category.objects.get(uuid=category_id)
    category.name = data.get('name')
    category.save()
    return jsonify(category.to_dict())


@app.route('/<category_id>', methods=['DELETE'])
@require_auth
@handle_error
def delete_category(category_id):
    Category.objects.get(uuid=category_id).delete()
    return ''
