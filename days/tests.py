from datetime import date, datetime
import unittest
from unittest import mock
from .foreign_trips import ForeignTrip, ForeignTripList, DuplicateTripError


class ForeignTripTestCase(unittest.TestCase):
    def test_constructor_stores_date_attributes_as_dates(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip = ForeignTrip(departure_date, return_date)
        self.assertIsInstance(trip.departure_date, date)
        self.assertNotIsInstance(trip.departure_date, datetime)
        self.assertIsInstance(trip.return_date, date)
        self.assertNotIsInstance(trip.return_date, datetime)

    def test_constructor_stores_datetime_arguments_as_dates(self):
        departure_date = datetime(2015, 10, 21)
        return_date = datetime(2015, 10, 25)
        trip = ForeignTrip(departure_date, return_date)
        self.assertIsInstance(trip.departure_date, date)
        self.assertNotIsInstance(trip.departure_date, datetime)
        self.assertIsInstance(trip.return_date, date)
        self.assertNotIsInstance(trip.return_date, datetime)

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

    def test_lt_returns_true_based_on_departure_date(self):
        departure_date_one = date(2015, 10, 20)
        return_date_one = date(2015, 10, 28)
        trip_one = ForeignTrip(departure_date_one, return_date_one)
        departure_date_two = date(2015, 10, 21)
        return_date_two = date(2015, 10, 25)
        trip_two = ForeignTrip(departure_date_two, return_date_two)
        self.assertTrue(trip_one < trip_two)

    def test_lt_returns_false_based_on_departure_date(self):
        departure_date_one = date(2015, 10, 20)
        return_date_one = date(2015, 10, 28)
        trip_one = ForeignTrip(departure_date_one, return_date_one)
        departure_date_two = date(2015, 10, 21)
        return_date_two = date(2015, 10, 25)
        trip_two = ForeignTrip(departure_date_two, return_date_two)
        self.assertFalse(trip_two < trip_one)

    def test_lt_returns_false_for_equal_trips(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip_one = ForeignTrip(departure_date, return_date)
        trip_two = ForeignTrip(departure_date, return_date)
        self.assertFalse(trip_one < trip_two)

    def test_le_returns_true_based_on_departure_date(self):
        departure_date_one = date(2015, 10, 20)
        return_date_one = date(2015, 10, 28)
        trip_one = ForeignTrip(departure_date_one, return_date_one)
        departure_date_two = date(2015, 10, 21)
        return_date_two = date(2015, 10, 25)
        trip_two = ForeignTrip(departure_date_two, return_date_two)
        self.assertTrue(trip_one <= trip_two)

    def test_le_returns_false_based_on_departure_date(self):
        departure_date_one = date(2015, 10, 20)
        return_date_one = date(2015, 10, 28)
        trip_one = ForeignTrip(departure_date_one, return_date_one)
        departure_date_two = date(2015, 10, 21)
        return_date_two = date(2015, 10, 25)
        trip_two = ForeignTrip(departure_date_two, return_date_two)
        self.assertFalse(trip_two <= trip_one)

    def test_le_returns_true_for_equal_trips(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip_one = ForeignTrip(departure_date, return_date)
        trip_two = ForeignTrip(departure_date, return_date)
        self.assertTrue(trip_one <= trip_two)

    def test_gt_returns_true_based_on_departure_date(self):
        departure_date_one = date(2015, 10, 20)
        return_date_one = date(2015, 10, 28)
        trip_one = ForeignTrip(departure_date_one, return_date_one)
        departure_date_two = date(2015, 10, 21)
        return_date_two = date(2015, 10, 25)
        trip_two = ForeignTrip(departure_date_two, return_date_two)
        self.assertTrue(trip_two > trip_one)

    def test_gt_returns_false_based_on_departure_date(self):
        departure_date_one = date(2015, 10, 20)
        return_date_one = date(2015, 10, 28)
        trip_one = ForeignTrip(departure_date_one, return_date_one)
        departure_date_two = date(2015, 10, 21)
        return_date_two = date(2015, 10, 25)
        trip_two = ForeignTrip(departure_date_two, return_date_two)
        self.assertFalse(trip_one > trip_two)

    def test_gt_returns_false_for_equal_trips(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip_one = ForeignTrip(departure_date, return_date)
        trip_two = ForeignTrip(departure_date, return_date)
        self.assertFalse(trip_one > trip_two)

    def test_ge_returns_true_based_on_departure_date(self):
        departure_date_one = date(2015, 10, 20)
        return_date_one = date(2015, 10, 28)
        trip_one = ForeignTrip(departure_date_one, return_date_one)
        departure_date_two = date(2015, 10, 21)
        return_date_two = date(2015, 10, 25)
        trip_two = ForeignTrip(departure_date_two, return_date_two)
        self.assertTrue(trip_two >= trip_one)

    def test_ge_returns_false_based_on_departure_date(self):
        departure_date_one = date(2015, 10, 20)
        return_date_one = date(2015, 10, 28)
        trip_one = ForeignTrip(departure_date_one, return_date_one)
        departure_date_two = date(2015, 10, 21)
        return_date_two = date(2015, 10, 25)
        trip_two = ForeignTrip(departure_date_two, return_date_two)
        self.assertFalse(trip_one >= trip_two)

    def test_ge_returns_true_for_equal_trips(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 25)
        trip_one = ForeignTrip(departure_date, return_date)
        trip_two = ForeignTrip(departure_date, return_date)
        self.assertTrue(trip_one >= trip_two)


class ForeignTripListTestCase(unittest.TestCase):
    def test_constructor_will_create_empty_sequence(self):
        trip_list = ForeignTripList()
        self.assertEqual(len(trip_list), 0)

    def test_constructor_will_create_sequence_of_foreigntrip_instances(self):
        departure_date_one = date(2015, 10, 20)
        departure_date_two = date(2015, 10, 21)
        return_date_one = date(2015, 10, 25)
        return_date_two = date(2015, 10, 28)
        trip_one = ForeignTrip(departure_date_one, return_date_one)
        trip_two = ForeignTrip(departure_date_two, return_date_two)
        trip_list = ForeignTripList([trip_one, trip_two])
        self.assertIn(trip_one, trip_list)
        self.assertIn(trip_two, trip_list)
        self.assertEqual(len(trip_list), 2)

    def test_constructor_will_not_accept_non_foreigntrip_items(self):
        with self.assertRaises(ValueError):
            ForeignTripList(["Not a ForeignTrip"])

    def test_constructor_sorts_returned_list(self):
        trip_1 = ForeignTrip(date(2016, 1, 1), date(2016, 1, 30))
        trip_2 = ForeignTrip(date(2016, 1, 2), date(2016, 1, 30))
        trip_3 = ForeignTrip(date(2016, 1, 3), date(2016, 1, 25))
        trip_4 = ForeignTrip(date(2016, 1, 4), date(2016, 1, 27))
        trip_5 = ForeignTrip(date(2016, 1, 5), date(2016, 1, 27))
        trip_list = ForeignTripList([trip_1, trip_5, trip_3, trip_2, trip_4])
        self.assertEqual(trip_list,
                    ForeignTripList([trip_1, trip_2, trip_3, trip_4, trip_5]))

    def test_total_days_gone_sums_days_gone_for_each_foreign_trip(self):
        three_day_trip = ForeignTrip(date(2015, 10, 21), date(2015, 10, 25))
        no_day_trip  = ForeignTrip(date(2015, 10, 26), date(2015, 10, 27))
        one_day_trip = ForeignTrip(date(2015, 10, 28), date(2015, 10, 30))

        trip_list = ForeignTripList([three_day_trip, no_day_trip, one_day_trip])
        self.assertEqual(trip_list.total_days_gone, 4)

    def test_insert_trip_adds_trip_to_original_list(self):
        trip_one = ForeignTrip(date(2015, 10, 20), date(2015, 10, 21))
        trip_two = ForeignTrip(date(2015, 10, 25), date(2015, 10, 28))

        trip_list = ForeignTripList([trip_one])
        trip_list.insert_trip(trip_two)
        self.assertIn(trip_two, trip_list)
        self.assertIn(trip_one, trip_list)

    def test_insert_trip_with_duplicate_raises_duplicatetriperror_and_does_not_add_duplicate(self):
        departure_date = date(2015, 10, 21)
        return_date = date(2015, 10, 22)
        trip = ForeignTrip(departure_date, return_date)
        identical_trip = ForeignTrip(departure_date, return_date)

        trip_list = ForeignTripList([trip])
        with self.assertRaises(DuplicateTripError):
            trip_list.insert_trip(identical_trip)
        self.assertEqual(len(trip_list), 1)

    def test_insert_trip_maintains_list_sorting(self):
        trip_1 = ForeignTrip(date(2016, 1, 1), date(2016, 1, 15))
        trip_2 = ForeignTrip(date(2016, 2, 2), date(2016, 2, 15))
        trip_3 = ForeignTrip(date(2016, 3, 3), date(2016, 3, 15))
        trip_list = ForeignTripList([trip_1, trip_3])
        trip_list.insert_trip(trip_2)
        self.assertEqual(trip_list[0], trip_1)
        self.assertEqual(trip_list[1], trip_2)
        self.assertEqual(trip_list[2], trip_3)
