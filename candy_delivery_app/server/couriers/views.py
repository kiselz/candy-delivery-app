"""Couriers views"""
from flask import request
from flask import jsonify
from flask import make_response
from flask import Blueprint
import candy_delivery_app.database.db as db
from .validation import has_all_parameters
from .validation import has_bad_property
from candy_delivery_app.server.orders.logic import is_order_suitable

blueprint = Blueprint('couriers', __name__)


@blueprint.route('/couriers', methods=('POST',))
def load_couriers():
    data = request.get_json()

    bad_couriers = []
    valid_couriers = []

    if data.get('data', None) is None:
        return make_response(
            jsonify({}), 400
        )

    couriers = data['data']
    for courier in couriers:
        if has_all_parameters(courier):
            if db.row_exists(
                    table_name='courier',
                    column_name='courier_id',
                    column_value=courier['courier_id']):
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
                         for courier in bad_couriers
                         if courier.get('courier_id', None) is not None]
                }
            }), 400
        )
    else:
        for courier in valid_couriers:
            db.create_courier(courier)

        return make_response(
            jsonify({
                'couriers':
                    [{'id': courier['courier_id']}
                     for courier in valid_couriers]
            }), 201
        )


@blueprint.route('/couriers/<int:courier_id>', methods=('GET', 'PATCH',))
def action_with_courier(courier_id):
    if request.method == 'PATCH':
        properties_to_update = request.get_json()
        courier = db.get_courier(courier_id)
        if courier is None or has_bad_property(courier):
            return make_response(
                jsonify(
                    {}
                )
            ), 400

        # Get rid of not relevant properties
        for key in list(properties_to_update.keys()):
            if key not in courier:
                del properties_to_update[key]

        courier.update(properties_to_update)
        db.update_courier(courier)

        del courier['rating'], courier['earnings']

        orders = db.get_courier_orders(courier)
        for order in orders:
            if not(is_order_suitable(courier, order)) and \
                    not(db.is_order_completed(order)):
                db.untie_order_from_courier(order, courier)

        return make_response(
            jsonify(courier), 200
        )
    elif request.method == 'GET':
        pass
