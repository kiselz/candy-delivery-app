"""Orders views"""
from flask import request
from flask import jsonify
from flask import make_response
from flask import Blueprint
import candy_delivery_app.database.db as db
from .validation import has_all_parameters


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
                    unique_name='order_id',
                    unique_value=order['order_id']):
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
                    'couriers':
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
                'couriers':
                    [{'id': order['order_id']}
                     for order in valid_orders]
            }), 201
        )


@blueprint.route('/orders/assign', methods=('POST',))
def assign_orders():
    pass


@blueprint.route('/orders/complete', methods=('POST',))
def complete_order():
    pass
