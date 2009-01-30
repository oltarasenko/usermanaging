"""
Package views are defined here.
"""


from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth import logout
from loginreg.forms import RegistrationForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from loginreg.models import UserProfile


def register_page(request):
    """
    View which implements registration. It uses forms decleared in the
    file forms.py. Provides user registation, password/username form validation
    """
    # Executed when user clicks submit to send his register data
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username = form.cleaned_data['username'],
                password = form.cleaned_data['pass1'],
                email = form.cleaned_data['email'])
            profile = UserProfile(user=user, about=form.cleaned_data['about'])
            return HttpResponseRedirect("/") # Returns 302 code
    # Show form for input (shown when user navigates to this page)
    else:
        form = RegistrationForm()
    variables = RequestContext(request, {'form': form})
    return render_to_response('registration/register.html', variables)


def logout_page(request):
    """
    Basic logout
    """
    logout(request)
    return HttpResponseRedirect("/")


def start_page(request):
    """
    Start page. Uses request context object to pass user specific data
    to the template.
    """
    return render_to_response('start_page.html', RequestContext(request))
