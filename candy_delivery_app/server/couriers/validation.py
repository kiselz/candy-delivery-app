def is_valid(courier):
    """
    Check whether given courier is valid
    :return bool
    """
    if courier.get('courier_id', None) is None:
        return False

    if courier.get('courier_type', None) is None:
        return False

    if courier.get('regions', None) is None:
        return False

    if courier.get('regions', None) is None:
        return False

    if courier.get('working_hours', None) is None:
        return False

    # Check if all parameters are valid
    if courier['courier_id'] <= 0:
        return False

    if courier['courier_type'] not in ('foot', 'bike', 'car'):
        return False

    bad_regions = list(filter(lambda x: x <= 0, courier['regions']))
    if len(bad_regions) > 0:
        return False

    for working_hour in courier['working_hours']:
        splitted_time = working_hour.split('-')

        if len(splitted_time) < 2:
            return False
        for time in splitted_time:
            hour, minute = None, None
            try:
                hour, minute = time.split(':')
            except ValueError:
                # Not in the format HH:MM
                return False

            if int(hour) >= 24 or int(hour) < 0:
                return False
            if int(minute) >= 59 or int(minute) < 0:
                return False

    return True
