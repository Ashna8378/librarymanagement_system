from django import forms
from .models import *
import re
from django.utils import timezone


class UserForm(forms.ModelForm):
    first_name = forms.CharField(label="First Name" ,widget=forms.TextInput(attrs={'class':'form-control','required':True ,  'autocomplete': 'off' ,'autocomplete':'autocomplete_off_randString', }),required=True,max_length=200)
    last_name = forms.CharField(label="Last Name" ,widget=forms.TextInput(attrs={'class':'form-control', 'required':False ,  'autocomplete': 'off' ,'autocomplete':'autocomplete_off_randString', }),required=False,max_length=200)
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','required':True,  'autocomplete': 'off' ,'autocomplete':'autocomplete_off_randString' }),required=True,max_length=200)
    email = forms.EmailField(label="Email ID" ,widget=forms.TextInput(attrs={'class':'form-control','required':True,  'autocomplete': 'off' ,'autocomplete':'autocomplete_off_randString' }),required=True,max_length=200)
    class Meta:
        model = User
        fields=['first_name','last_name','username','email']

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        valid_domains = ['gmail.com', 'yahoo.com', 'hotmail.com', 'live.com' , 'outlook.com', 'msn.com']  # Add more domains as needed

        if not email:
            self.add_error('email', 'Email is required.')
        elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            self.add_error('email', 'Enter a valid email address.')
        else:
            domain = email.split('@')[1]
            if domain not in valid_domains:
                self.add_error('email', 'Enter a valid email address')

        return cleaned_data