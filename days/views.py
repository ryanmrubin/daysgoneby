from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from .forms import DaysGoneCalculatorForm, N400SubmissionForm
from .foreign_trips import ForeignTrip, ForeignTripList


def calculate_days_gone(request):
    form = DaysGoneCalculatorForm()
    trip = None

    if request.method == "POST":
        form = DaysGoneCalculatorForm(request.POST)
        if form.is_valid():
            trip = ForeignTrip.build_from_form(form)

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
    trips_so_far = request.session.get('trips_so_far', ForeignTripList())

    if request.method == 'POST':
        if request.POST['submit'] == 'reset':
            request.session.pop('trips_so_far')
            request.session.pop('n400_date')
            return redirect(reverse('n400_home'))

        else:
            form = DaysGoneCalculatorForm(request.POST)
            if form.is_valid():
                trip = ForeignTrip.build_from_form(form)
                trips_so_far.insert_trip(trip)
                request.session['trips_so_far'] = trips_so_far

                form = DaysGoneCalculatorForm()

    total_days_gone = trips_so_far.total_days_gone
    context = {'submission_date': submission_date,
               'form': form,
               'trips_so_far': trips_so_far,
               'total_days_gone': total_days_gone}
    return render(request,'days/n400_date_entry.html', context)

    # redirect similar urls to the N-400/etc urls.
    # highlight days greater than 180 as needing further explanation
    # compare total days gone to the max number (if present for 913 OR MORE in 5 years prior to n-400 date, to they meet the req.)--colornumber and display note

    # add messages app so as to alert when some of the following happen
    # sort trips in trips_so_far
    # overlapping trips mean throw an error and tell to fix.
    # throw out days out of the country if they were more than 5 years prior to n-400 date
        # show whole trip but include a note. (put notes column in table--the 180+ shoulddo that too.)
        # in this event, show extra line--Total Days Gone in Statutory Period
    # if trip range includes date of n-400 submission, throw error saying to check date of submission
