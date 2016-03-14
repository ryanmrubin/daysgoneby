from collections import namedtuple


ForeignTrip = namedtuple('ForeignTrip', ('departure_date', 'return_date', 'days_gone'))


def days_out_of_country(departure_date, return_date):
    """
    Assumes dates are date instances. Travel days do not count as
    days out of the country.
    """
    return (return_date - departure_date).days - 1


def build_foreign_trip(departure_date, return_date):
    days_gone = days_out_of_country(departure_date, return_date)
    return ForeignTrip(departure_date, return_date, days_gone)


def build_foreign_trip_from_form(form):
    departure_date = form.cleaned_data['departure_date']
    return_date = form.cleaned_data['return_date']
    return build_foreign_trip(departure_date, return_date)


def insert_trip(trip, lst):
    lst.append(trip)


def get_total_days_gone(lst):
    return sum(trip.days_gone for trip in lst)
