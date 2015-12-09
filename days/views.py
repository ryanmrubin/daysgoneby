from django.shortcuts import render
from django.http import HttpResponse
from .forms import DaysGoneCalculatorForm


def calculate_days_gone(request):
    form = DaysGoneCalculatorForm()
    result_data = {}
    if request.method == "POST":
        form = DaysGoneCalculatorForm(request.POST)
        if form.is_valid():
            departure_date = form.cleaned_data['departure_date']
            return_date = form.cleaned_data['return_date']
            result_data['days_gone'] = (return_date - departure_date).days - 1 # neither travel day counts

            result_data['departure_date'] = departure_date
            result_data['return_date'] = return_date

    return render(request, 'days/days_gone_calculator.html', dict(form=form, result_data=result_data))
