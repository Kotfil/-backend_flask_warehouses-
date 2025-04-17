from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from

from app.models import db, Warehouse, User
from app.schemas import WarehouseSchema
from app.services.rbac import is_admin, is_manager, is_warehouse_manager

bp = Blueprint('warehouses', __name__, url_prefix='/warehouses')


@bp.route('/', methods=['GET'])
@swag_from({
    'tags': ['Warehouses'],
    'summary': 'Get all warehouses',
    'responses': {
        200: {
            'description': 'List of all warehouses',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'integer'},
                        'name': {'type': 'string'},
                        'area': {'type': 'number'},
                        'price': {'type': 'number'},
                        'manager_id': {'type': 'integer'}
                    }
                }
            }
        }
    }
})
def list_warehouses():
    warehouses = Warehouse.query.all()
    return WarehouseSchema(many=True).dump(warehouses), 200


@bp.route('/', methods=['POST'])
@jwt_required()
@swag_from({
    'tags': ['Warehouses'],
    'summary': 'Create a warehouse',
    'parameters': [{
        'name': 'body',
        'in': 'body',
        'required': True,
        'schema': {
            'type': 'object',
            'properties': {
                'name': {'type': 'string'},
                'area': {'type': 'number'},
                'price': {'type': 'number'},
                'manager_id': {'type': 'integer'}
            },
            'example': {
                'name': 'Central Storage',
                'area': 150.0,
                'price': 7500.0,
                'manager_id': None
            }
        }
    }],
    'responses': {
        201: {
            'description': 'Warehouse created',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer'},
                    'name': {'type': 'string'},
                    'area': {'type': 'number'},
                    'price': {'type': 'number'},
                    'manager_id': {'type': 'integer'}
                }
            }
        }
    }
})
def create_warehouse():
    user = User.query.get(get_jwt_identity())
    if not (is_admin(user) or is_manager(user)):
        return {"msg": "Forbidden"}, 403

    data = request.get_json()
    warehouse = Warehouse(**data)
    db.session.add(warehouse)
    db.session.commit()
    return WarehouseSchema().dump(warehouse), 201


@bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
@swag_from({
    'tags': ['Warehouses'],
    'summary': 'Update warehouse',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'integer',
            'required': True
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'area': {'type': 'number'},
                    'price': {'type': 'number'},
                    'manager_id': {'type': 'integer'}
                },
                'example': {
                    'name': 'Updated Warehouse',
                    'area': 200,
                    'price': 8800,
                    'manager_id': 2
                }
            }
        }
    ],
    'responses': {
        200: {'description': 'Warehouse updated'}
    }
})
def update_warehouse(id):
    user = User.query.get(get_jwt_identity())
    warehouse = Warehouse.query.get_or_404(id)

    if not (is_admin(user) or is_warehouse_manager(user, warehouse)):
        return {"msg": "Forbidden"}, 403

    data = request.get_json()
    for key, value in data.items():
        setattr(warehouse, key, value)
    db.session.commit()
    return WarehouseSchema().dump(warehouse), 200


@bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
@swag_from({
    'tags': ['Warehouses'],
    'summary': 'Delete warehouse',
    'parameters': [{
        'name': 'id',
        'in': 'path',
        'type': 'integer',
        'required': True
    }],
    'responses': {
        204: {'description': 'Warehouse deleted'}
    }
})
def delete_warehouse(id):
    warehouse = Warehouse.query.get_or_404(id)
    db.session.delete(warehouse)
    db.session.commit()
    return '', 204
