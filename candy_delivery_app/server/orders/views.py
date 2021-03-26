"""Orders views"""
from flask import Blueprint


blueprint = Blueprint('orders', __name__)


@blueprint.route('/orders', methods=('POST',))
def load_orders():
    pass


@blueprint.route('/orders/assign', methods=('POST',))
def assign_orders():
    pass


@blueprint.route('/orders/complete', methods=('POST',))
def complete_order():
    pass
