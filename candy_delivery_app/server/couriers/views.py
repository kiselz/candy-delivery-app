"""Couriers views"""
from flask import request
from flask import jsonify
from flask import make_response
from flask import Blueprint
from candy_delivery_app.database.db import create_courier
from candy_delivery_app.database.db import row_exists
from .validation import has_all_parameters

blueprint = Blueprint('couriers', __name__)


@blueprint.route('/couriers', methods=('POST',))
def load_couriers():
    data = request.get_json()

    bad_couriers = []
    valid_couriers = []

    couriers = data['data']
    for courier in couriers:
        if has_all_parameters(courier):
            if row_exists('courier', 'id', courier['courier_id']):
                # This courier is already in the table
                # There is another handler to update it
                bad_couriers.append(courier)
            else:
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
        for courier in valid_couriers:
            create_courier(courier)

        return make_response(
            jsonify({
                'couriers':
                    [{'id': courier['courier_id']}
                     for courier in valid_couriers]
            }), 201
        )


@blueprint.route('/couriers/<int:courier_id>', methods=('GET', 'PATCH',))
def action_with_courier():
    if request.method == 'PATCH':
        pass
    elif request.method == 'GET':
        pass
