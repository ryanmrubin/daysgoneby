import datetime as dt


def get_statutory_start_date(submission_date):
    """
    Gets the date five years prior to submission_date, such that days
    present/absent are calculated after this date and up to/including
    submision date.
    Assumes submission_date is a datetime.date instance.
    """
    return dt.date(submission_date.year - 5,
                   submission_date.month,
                   submission_date.day)
