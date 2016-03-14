from django import forms
from django.core.exceptions import ValidationError


class DaysGoneCalculatorForm(forms.Form):
    departure_date = forms.DateField(help_text="MM/DD/YYYY")
    return_date = forms.DateField(help_text="MM/DD/YYYY")

    def clean(self):
        cleaned_data = super(DaysGoneCalculatorForm, self).clean()
        departure_date = cleaned_data.get('departure_date', None)
        return_date = cleaned_data.get('return_date', None)
        if return_date and departure_date and return_date <= departure_date:
            raise ValidationError("Please enter a departure date prior to the return date.")

class N400SubmissionForm(forms.Form):
    submission_date = forms.DateField(help_text="MM/DD/YYYY",
                                      label="N-400 Submission Date")
