"""Orders views"""
from flask import request
from flask import jsonify
from flask import make_response
from flask import Blueprint
import candy_delivery_app.database.db as db
from .validation import has_all_parameters
from .logic import is_order_suitable
from datetime import datetime


blueprint = Blueprint('orders', __name__)


@blueprint.route('/orders', methods=('POST',))
def load_orders():
    data = request.get_json()

    bad_orders = []
    valid_orders = []

    orders = data['data']
    for order in orders:
        if has_all_parameters(order):
            if db.row_exists(
                    table_name='orders',
                    column_name='order_id',
                    column_value=order['order_id']):
                # This courier is already in the table
                # There is another handler to update it
                bad_orders.append(order)
            else:
                valid_orders.append(order)
        else:
            bad_orders.append(order)

    if len(bad_orders) > 0:
        return make_response(
            jsonify({
                'validation_error': {
                    'orders':
                        [{'id': order['order_id']}
                         for order in bad_orders]
                }
            }), 400
        )
    else:
        for order in valid_orders:
            db.create_order(order)

        return make_response(
            jsonify({
                'orders':
                    [{'id': order['order_id']}
                     for order in valid_orders]
            }), 201
        )


@blueprint.route('/orders/assign', methods=('POST',))
def assign_orders():
    data = request.get_json()

    courier = db.get_courier(data['courier_id'])
    if courier is None:
        return make_response(jsonify({}), 400)

    unassigned_orders = db.get_all_unassigned_orders()

    suitable_orders = []
    for order in unassigned_orders:
        if is_order_suitable(courier, order):
            suitable_orders.append(order)

    if len(suitable_orders) > 0:
        assign_time = datetime.now().isoformat(timespec='seconds')
        for order in suitable_orders:
            db.sign_order_to_courier(order, courier)

        return make_response(
            jsonify({
                'orders':
                    [{'id': order['order_id']}
                     for order in suitable_orders],
                'assign_time': assign_time,
            }), 200
        )
    else:
        return make_response(
            jsonify({
                'orders': []
            }), 200
        )


@blueprint.route('/orders/complete', methods=('POST',))
def complete_order():
    pass
