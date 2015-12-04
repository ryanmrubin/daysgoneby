from django import forms


class DaysGoneCalculatorForm(forms.Form):
    departure_date = forms.DateField()
    return_date = forms.DateField()

