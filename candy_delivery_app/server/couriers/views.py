"""Couriers views"""
from flask import request
from flask import Blueprint


blueprint = Blueprint('couriers', __name__)


@blueprint.route('/couriers', methods=('POST',))
def load_couriers():
    pass


@blueprint.route('/couriers/<int:courier_id>', methods=('GET', 'PATCH',))
def action_with_courier():
    pass
