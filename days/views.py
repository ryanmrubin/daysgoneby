from django.shortcuts import render
from django.http import HttpResponse
from .forms import DaysGoneCalculatorForm


def calculate_days_gone(request):
    form = DaysGoneCalculatorForm()
    result = 0
    if request.method == "POST":
        form = DaysGoneCalculatorForm(request.POST)
        if form.is_valid():
            departure_date = form.cleaned_data['departure_date']
            return_date = form.cleaned_data['return_date']
            result = (return_date - departure_date).days - 1 # neither travel day counts

    return render(request, 'days/days_gone_calculator.html', dict(form=form, result=result))
