def days_out_of_country(departure_date, return_date):
    """
    Assumes dates are date instances. Travel days do not count as
    days out of the country.
    """
    return (return_date - departure_date).days - 1
