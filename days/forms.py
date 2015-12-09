from django import forms
from django.core.exceptions import ValidationError


class DaysGoneCalculatorForm(forms.Form):
    departure_date = forms.DateField(help_text="MM/DD/YYYY")
    return_date = forms.DateField(help_text="MM/DD/YYYY")

    def clean(self):
        cleaned_data = super(DaysGoneCalculatorForm, self).clean()
        departure_date = cleaned_data['departure_date']
        return_date = cleaned_data['return_date']
        if not departure_date < return_date:
            raise ValidationError("Please enter a departure date prior to the return date.")

