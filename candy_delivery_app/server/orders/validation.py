def has_all_parameters(order):
    """
    Check whether given order is has all parameters
    and they are valid.
    """

    if order.get('order_id', None) is None:
        return False

    if order.get('weight', None) is None:
        return False

    if order.get('region', None) is None:
        return False

    if order.get('delivery_hours', None) is None:
        return False

    # Check if all parameters are valid
    checks = (
        is_order_id_valid,
        is_weight_valid,
        is_region_valid,
        are_delivery_hours_valid
    )

    for check in checks:
        if not (check(order)):
            return False

    return True


def is_order_id_valid(order):
    return order['order_id'] > 0


def is_weight_valid(order):
    return order['weight'] >= 0.01 and order['weight'] <= 50


def is_region_valid(order):
    return order['region'] > 0


def are_delivery_hours_valid(order):
    for delivery_hour in order['delivery_hours']:
        split_time = delivery_hour.split('-')

        if len(split_time) < 2:
            return False
        for time in split_time:
            hour, minute = None, None
            try:
                hour, minute = time.split(':')
            except ValueError:
                # Not in the format HH:MM
                return False

            if int(hour) > 23 or int(hour) < 0:
                return False
            if int(minute) > 59 or int(minute) < 0:
                return False
    return True
