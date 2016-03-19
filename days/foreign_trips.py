import datetime as dt

class ForeignTrip():
    def __init__(self, departure_date, return_date):
        super().__init__()

        if isinstance(departure_date, dt.datetime):
            departure_date = departure_date.date()
        if isinstance(return_date, dt.datetime):
            return_date = return_date.date()

        self.departure_date = departure_date
        self.return_date = return_date

    def __eq__(self, other):
        return (self.departure_date == other.departure_date
            and self.return_date == other.return_date)

    def __contains__(self, other_date):
        if isinstance(other_date, dt.datetime):
            other_date = other_date.date()

        return (other_date >= self.departure_date
            and other_date <= self.return_date)

    def __repr__(self):
        return 'ForeignTrip(%s, %s)' % (self.departure_date, self.return_date)

    @property
    def days_gone(self):
        """
        Assumes dates are date instances.
        Travel days do not count as days out of the country.
        """
        if not hasattr(self, '_days_gone'):
            self._days_gone = (self.return_date - self.departure_date).days - 1
        return self._days_gone

    @classmethod
    def build_from_form(cls, form):
        departure_date = form.cleaned_data['departure_date']
        return_date = form.cleaned_data['return_date']
        return cls(departure_date, return_date)


class ForeignTripList(list):
    def insert_trip(self, trip):
        self.append(trip)

    @property
    def total_days_gone(self):
        return sum(trip.days_gone for trip in self)


class DuplicateTripError(ValueError):
    pass
