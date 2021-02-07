from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from plats_bank.models import City, Job_type

User = get_user_model()


class UserLoginForm(forms.Form):
    # email = forms.EmailField()
    # password = forms.PasswordInput()
    email = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password')
        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Fel user-ID eller lösenord')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Fel user-ID eller lösenord')
            user = authenticate(email=email, password=password)

            if not user:
                raise forms.ValidationError('User är inte active')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('email',)

class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), label='', required=True)
    job_type = forms.ModelChoiceField(queryset=Job_type.objects.all(), label='', required=True)
    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput,label='Skicka mail')

    job_type.widget.attrs.update({'class': 'selectpicker mx-2 my-1 mr-sm-2',
                                  'data-live-search': 'true', })
    city.widget.attrs.update({'class': 'selectpicker my-1 mr-sm-2',
                              'data-live-search': 'true'})

    class Meta:
        model = User
        fields = ('city','jobb_type','send_email')