from django.shortcuts import render
from django.views.generic import View
from .forms import DaysGoneCalculatorForm
from .utils import days_out_of_country, ForeignTrip, insert_trip, get_total_days_gone


def calculate_days_gone(request):
    form = DaysGoneCalculatorForm()
    result_data = {}

    if request.method == "POST":
        form = DaysGoneCalculatorForm(request.POST)
        if form.is_valid():
            departure_date = form.cleaned_data['departure_date']
            return_date = form.cleaned_data['return_date']
            result_data['days_gone'] = days_out_of_country(departure_date,
                                                           return_date)
            result_data['departure_date'] = departure_date
            result_data['return_date'] = return_date

    context = {'form': form,
               'result_data': result_data}
    return render(request, 'days/days_gone_calculator.html', context)


class N400View(View):
    # compare total days gone to the max number (913? for 2.5 years?)
    # add form to add date of n-400 application
    # throw out days out of the country if they were before n-400 date (dobule-check with Mia)
    # calculate the 913(?) days out of the 5 years from that n-400 date forward.
    # sort trips in trips_so_far
    # handle overlapping trips
    def get(self, request, *args, **kwargs):
        form = DaysGoneCalculatorForm()
        trips_so_far = request.session.get('trips_so_far', [])
        total_days_gone = get_total_days_gone(trips_so_far)
        context = {'form': form,
                   'trips_so_far': trips_so_far,
                   'total_days_gone': total_days_gone}
        return render(request,'days/multiple_trips.html', context)

    def post(self, request, *args, **kwargs):
        form = DaysGoneCalculatorForm()
        trips_so_far = request.session.get('trips_so_far', [])

        if request.POST['submit'] == 'reset':
            trips_so_far = request.session['trips_so_far'] = []

        else:
            form = DaysGoneCalculatorForm(request.POST)
            if form.is_valid():
                departure_date = form.cleaned_data['departure_date']
                return_date = form.cleaned_data['return_date']
                days_gone = days_out_of_country(departure_date, return_date)

                insert_trip(ForeignTrip(departure_date, return_date, days_gone),
                            trips_so_far)
                request.session['trips_so_far'] = trips_so_far
                form = DaysGoneCalculatorForm()

        total_days_gone = get_total_days_gone(trips_so_far)
        context = {'form': form,
                   'trips_so_far': trips_so_far,
                   'total_days_gone': total_days_gone}
        return render(request,'days/multiple_trips.html', context)
