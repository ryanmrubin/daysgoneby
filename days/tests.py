from datetime import date, datetime
import unittest
from unittest import mock
from .foreign_trips import ForeignTrip, ForeignTripList


class ForeignTripTestCase(unittest.TestCase):
    def test_days_gone_does_not_count_travel_dates(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip = ForeignTrip(departure_date, return_date)
        self.assertEqual(trip.days_gone, 3)

    def test_days_gone_returns_zero_when_travel_dates_are_consecutive(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 22)
        trip = ForeignTrip(departure_date, return_date)
        self.assertEqual(trip.days_gone, 0)

    def test_days_gone_counts_feb_29_on_leap_years(self):
        departure_date = date(2012, 2, 28)
        return_date = date(2012, 3, 1)
        trip = ForeignTrip(departure_date, return_date)
        self.assertEqual(trip.days_gone, 1)

    def test_days_gone_does_not_count_feb_29_on_non_leap_years(self):
        departure_date = date(2013, 2, 28)
        return_date = date(2013, 3, 1)
        trip = ForeignTrip(departure_date, return_date)
        self.assertEqual(trip.days_gone, 0)

    def test_build_from_form_gets_correct_dates_from_forms_cleaned_data(self):
        departure_date = date(1985, 10, 21)
        return_date = date(2015, 10, 21)
        form = mock.Mock(cleaned_data={'departure_date': departure_date,
                                       'return_date': return_date})
        trip = ForeignTrip.build_from_form(form)

        self.assertEqual(trip.departure_date, departure_date)
        self.assertEqual(trip.return_date, return_date)

    def test_contains_date_within_range(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip = ForeignTrip(departure_date, return_date)

        included_date = date(2015, 10, 23)
        self.assertIn(included_date, trip)

    def test_does_not_contain_date_outside_range(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip = ForeignTrip(departure_date, return_date)

        outside_date = date(2015, 10, 28)
        self.assertNotIn(outside_date, trip)

    def test_contains_departure_date(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip = ForeignTrip(departure_date, return_date)
        self.assertIn(departure_date, trip)

    def test_contains_return_date(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip = ForeignTrip(departure_date, return_date)
        self.assertIn(return_date, trip)

    def test_contains_works_on_datetimes(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip = ForeignTrip(departure_date, return_date)

        included_datetime = datetime(2015, 10, 23, 0, 0)
        self.assertIn(included_datetime, trip)

    def test_equality_with_another_trip_with_same_departure_and_return_dates(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip_one = ForeignTrip(departure_date, return_date)
        trip_two = ForeignTrip(departure_date, return_date)
        self.assertEqual(trip_one, trip_two)

    def test_inequality_with_another_trip_with_different_departure_date(self):
        departure_date_one = date(2015, 10, 20)
        departure_date_two = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip_one = ForeignTrip(departure_date_one, return_date)
        trip_two = ForeignTrip(departure_date_two, return_date)
        self.assertNotEqual(trip_one, trip_two)

    def test_inequality_with_another_trip_with_different_return_date(self):
        departure_date = date(2015, 10, 20)
        return_date_one = date(2015, 10, 25)
        return_date_two = date(2015, 10, 28)
        trip_one = ForeignTrip(departure_date, return_date_one)
        trip_two = ForeignTrip(departure_date, return_date_two)
        self.assertNotEqual(trip_one, trip_two)

    def test_inequality_with_another_trip_with_neither_date_in_common(self):
        departure_date_one = date(2015, 10, 20)
        departure_date_two = date(2015, 10, 21)
        return_date_one = date(2015, 10, 25)
        return_date_two = date(2015, 10, 28)
        trip_one = ForeignTrip(departure_date_one, return_date_one)
        trip_two = ForeignTrip(departure_date_two, return_date_two)
        self.assertNotEqual(trip_one, trip_two)

    def test_equality_with_another_trip_formed_with_datetimes(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        departure_datetime = datetime(2015, 10, 21)
        return_datetime = datetime(2015, 10, 25)

        trip_one = ForeignTrip(departure_date, return_date)
        trip_two = ForeignTrip(departure_datetime, return_datetime)
        self.assertEqual(trip_one, trip_two)


class ForeignTripListTestCase(unittest.TestCase):
    def test_total_days_gone_sums_days_gone_for_each_foreign_trip(self):
        three_day_trip = mock.Mock(days_gone=3)
        no_day_trip = mock.Mock(days_gone=0)
        one_day_trip = mock.Mock(days_gone=1)
        trip_list = ForeignTripList([three_day_trip, no_day_trip, one_day_trip])
        self.assertEqual(trip_list.total_days_gone, 4)
