def has_all_parameters(courier):
    """
    Check whether given courier is has all parameters
    and they are valid.
    :return bool
    """
    if courier.get('id', None) is None:
        return False

    if courier.get('courier_type_id', None) is None:
        return False

    if courier.get('regions', None) is None:
        return False

    if courier.get('working_hours', None) is None:
        return False

    # Check if all parameters are valid

    checks = (
        is_courier_id_valid,
        is_courier_type_valid,
        are_regions_valid,
    )

    for check in checks:
        if not (check(courier)):
            return False

    return True


def has_bad_property(dictionary):
    for key in dictionary:
        if key not in \
                ('id', 'courier_type_id', 'rating',
                 'regions', 'working_hours', 'earnings',
                 'courier_id',):
            return True
    return False


def is_courier_id_valid(courier):
    return courier['id'] > 0


def is_courier_type_valid(courier):
    return courier['courier_type_id'] in (1, 2, 3)


def are_regions_valid(courier):
    bad_regions = list(filter(lambda x: x <= 0, courier['regions']))
    return len(bad_regions) == 0


def are_working_hours_valid(courier):
    for working_hour in courier['working_hours']:
        split_time = working_hour.split('-')

        if len(split_time) < 2:
            return False
        for time in split_time:
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
