from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .forms import DaysGoneCalculatorForm, N400SubmissionForm
from .utils import build_foreign_trip_from_form, insert_trip, get_total_days_gone


def calculate_days_gone(request):
    form = DaysGoneCalculatorForm()
    trip = None

    if request.method == "POST":
        form = DaysGoneCalculatorForm(request.POST)
        if form.is_valid():
            trip = build_foreign_trip_from_form(form)

    context = {'form': form,
               'trip': trip}
    return render(request, 'days/days_gone_calculator.html', context)


def n400_home(request):
    submission_date = request.session.get('n400_date', None)
    if submission_date:
        return redirect(reverse('n400_date_entry'))

    form = N400SubmissionForm()

    if request.method == 'POST':
        form = N400SubmissionForm(request.POST)
        if form.is_valid():
            request.session['n400_date'] = form.cleaned_data['submission_date']
            return redirect(reverse('n400_date_entry'))

    context = {'form': form}
    return render(request, 'days/n400_home.html', context)


def n400_date_entry(request):
    submission_date = request.session.get('n400_date', None)
    if submission_date is None:
        return redirect(reverse('n400_home'))

    form = DaysGoneCalculatorForm()
    trips_so_far = request.session.get('trips_so_far', [])

    if request.method == 'POST':
        if request.POST['submit'] == 'reset':
            request.session.pop('trips_so_far')
            request.session.pop('n400_date')
            return redirect(reverse('n400_home'))

        else:
            form = DaysGoneCalculatorForm(request.POST)
            if form.is_valid():
                trip = build_foreign_trip_from_form(form)
                insert_trip(trip, trips_so_far)
                request.session['trips_so_far'] = trips_so_far

                form = DaysGoneCalculatorForm()

    total_days_gone = get_total_days_gone(trips_so_far)
    context = {'submission_date': submission_date,
               'form': form,
               'trips_so_far': trips_so_far,
               'total_days_gone': total_days_gone}
    return render(request,'days/n400_date_entry.html', context)

    # redirect similar urls to the N-400/etc urls.
    # highlight days greater than 180 as needing further explanation
    # compare total days gone to the max number (913? for 2.5 years?) and display note, along with coloring text appropriately

    # validate N400 submission not in the future (and more than 5 years ago? ask Mia.)
    # add messages app so as to alert when some of the following happen
    # sort trips in trips_so_far
    # handle overlapping trips
    # throw out days out of the country if they were before n-400 date (dobule-check with Mia)
    # throw out days out of the country if they were more than 5 years from n-400 date (double-check with Mia)
    # calculate the 913(?) days out of the 5 years from that n-400 date forward.
