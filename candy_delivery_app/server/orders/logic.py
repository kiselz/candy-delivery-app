"""Functions that deal with orders logic"""
from datetime import datetime
import candy_delivery_app.database.db as db


def is_order_suitable(courier, order):
    """
    Check whether the order is suitable to the courier
    """

    max_weight = db.get_courier_type_weight(
        db.get_courier_type_id(courier['courier_type'])
    )

    if order['weight'] > max_weight:
        return False

    if order['region'] not in courier['regions']:
        return False

    current_year = int(datetime.now().year)
    current_month = int(datetime.now().month)
    current_day = int(datetime.now().day)

    for working_hour in map(lambda x: x.split('-'),
                            courier['working_hours']):

        work_start = datetime(year=current_year,
                              month=current_month,
                              day=current_day,
                              hour=int(working_hour[0][:2]),
                              minute=int(working_hour[0][3:])
                              )
        work_end = datetime(year=current_year,
                            month=current_month,
                            day=current_day,
                            hour=int(working_hour[1][:2]),
                            minute=int(working_hour[1][3:]),
                            )

        for delivery_hour in map(lambda x: x.split('-'),
                                 order['delivery_hours']):
            delivery_start = datetime(year=current_year,
                                      month=current_month,
                                      day=current_day,
                                      hour=int(delivery_hour[0][:2]),
                                      minute=int(delivery_hour[0][3:]),
                                      )
            delivery_end = datetime(year=current_year,
                                    month=current_month,
                                    day=current_day,
                                    hour=int(delivery_hour[1][:2]),
                                    minute=int(delivery_hour[1][3:]),
                                    )

            if work_start < delivery_end and work_end > delivery_start:
                return True
    return False
