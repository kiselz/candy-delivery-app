"""Couriers views"""
from flask import request
from flask import jsonify
from flask import make_response
from flask import Blueprint
from candy_delivery_app.database.db import create_courier
from .validation import is_valid

blueprint = Blueprint('couriers', __name__)


@blueprint.route('/couriers', methods=('POST',))
def load_couriers():
    data = request.get_json()

    bad_couriers = []
    valid_couriers = []

    couriers = data['data']
    for courier in couriers:
        if is_valid(courier):
            create_courier(courier)
            valid_couriers.append(courier)
        else:
            bad_couriers.append(courier)

    if len(bad_couriers) > 0:
        return make_response(
            jsonify({
                'validation_error': {
                    'couriers':
                        [{'id': courier['courier_id']}
                         for courier in bad_couriers]
                }
            }), 400
        )
    else:
        return make_response(
            jsonify({
                'couriers':
                    [{'id': courier['courier_id']}
                     for courier in valid_couriers]
            }), 201
        )


@blueprint.route('/couriers/<int:courier_id>', methods=('GET', 'PATCH',))
def action_with_courier():
    pass
