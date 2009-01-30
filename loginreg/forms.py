"""
This module implements, form for registration a new user,
provides 2 data validation methods
"""

from django import forms
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class RegistrationForm(forms.Form):
    '''
    The Register form is created to deal with registration process
    check if data is clean and passwords match each other
    '''
    username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label = 'Email')
    pass1 = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput())
    pass2 = forms.CharField(
        label = 'Password (Again)',
        widget = forms.PasswordInput())
    about = forms.CharField(required = False,
                            label = 'about',
                            widget=forms.Textarea)

    def clean_pass2(self):
        """
        Method used to check if passwords are matching each other
        """
        if 'pass1' in self.cleaned_data:
            pass1 = self.cleaned_data['pass1']
            pass2 = self.cleaned_data['pass2']
            if pass1 == pass2:
                return pass2
            raise forms.ValidationError("Please retype passwords. \
They didn't match")

    def clean_username(self):
        """
        Method to check if username conteins invalod data. Also checks
        if that username was already taken.
        """
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Error: Username can contains \
only alphanumeric characters')
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            return username
        raise forms.ValidationError('Username is already taken')
