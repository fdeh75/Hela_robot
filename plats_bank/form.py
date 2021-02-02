from django import forms

from plats_bank.models import City, Job_type


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), label='',required=False)
    job_type = forms.ModelChoiceField(queryset=Job_type.objects.all(), label='', required=False)

    job_type.widget.attrs.update({'class': 'selectpicker mx-2 my-1 mr-sm-2',
                                  'data-live-search': 'true',})
    city.widget.attrs.update({'class': 'selectpicker my-1 mr-sm-2',
                              'data-live-search': 'true'})
