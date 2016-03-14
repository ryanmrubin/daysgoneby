from collections import namedtuple


ForeignTrip = namedtuple('ForeignTrip', ('departure_date', 'return_date', 'days_gone'))


def days_out_of_country(departure_date, return_date):
    """
    Assumes dates are date instances. Travel days do not count as
    days out of the country.
    """
    return (return_date - departure_date).days - 1


def insert_trip(trip, lst):
    lst.append(trip)


def get_total_days_gone(lst):
    return sum(trip.days_gone for trip in lst)
