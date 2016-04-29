import bisect
import datetime as dt
from functools import total_ordering


class DuplicateTripError(ValueError):
    pass


class OverlappingTripError(ValueError):
    pass


@total_ordering
class ForeignTrip:
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

    def __lt__(self, other):
        return self.departure_date < other.departure_date

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

    def days_gone_between(self, start_date, end_date):
        """
        Returns days gone after start_date and before end_date.
        Assumes start_date and end_date are datetime.date instances.
        Start and end dates do not count as days gone.
        """
        if start_date < self.departure_date and end_date > self.return_date:
            return self.days_gone

        elif start_date in self and end_date in self:
            return (end_date - start_date).days - 1

        elif start_date in self:
            return (self.return_date - start_date).days - 1

        elif end_date in self:
            return (end_date - self.departure_date).days - 1

        else: # ranges don't overlap
            return 0

    @classmethod
    def build_from_form(cls, form):
        departure_date = form.cleaned_data['departure_date']
        return_date = form.cleaned_data['return_date']
        return cls(departure_date, return_date)


class ForeignTripList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if any(filter(lambda x: not isinstance(x, ForeignTrip), self)):
            raise ValueError("ForeignTripList must contain only "
                             "ForeignTrip instances.")
        self.sort()

    def insert_trip(self, trip):
        if trip in self:
            raise DuplicateTripError("ForeignTrip instances in a "
                                     "ForeignTripList must be unique.")
        insert_point = bisect.bisect(self, trip)

        try:
            trip_before = self[insert_point-1]
            if trip.departure_date in trip_before:
                raise OverlappingTripError("%s overlaps with %s."
                                           % (trip, trip_before))
        except IndexError:
            pass

        try:
            trip_after = self[insert_point]
            if trip.return_date in trip_after:
                raise OverlappingTripError("%s overlaps with %s."
                                           % (trip, trip_after))
        except IndexError:
            pass

        self.insert(insert_point, trip)

    @property
    def total_days_gone(self):
        return sum(trip.days_gone for trip in self)
