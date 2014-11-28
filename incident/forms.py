from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget

from models import Incident

class CreateIncidentForm(ModelForm):
    date = forms.DateField(("%m/%d/%Y",), widget=forms.DateInput(format="%m/%d/%Y", attrs={'class': 'datePicker',}), label='Date of Incident:')
    class Meta:
        model = Incident
        fields = ['position','what', 'date', 'time']
        # exclude = ("published", )
        # widgets = {
        #     "date": SelectDateWidget(),
        #     "time": SelectDateWidget(),
        # }

        # # The 'datepicker' ties to the jqueryui script at the bottom of incident_form
        # widgets = {
        #     # 'date': forms.DateInput(attrs={'class':'datepicker'}),
        #     'date': forms.DateInput(attrs={'class':'datepicker', 'size': 10, 'id': 'datepicker', }),
        # }