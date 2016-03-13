from django.shortcuts import render
from .forms import DaysGoneCalculatorForm
from .utils import days_out_of_country


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
