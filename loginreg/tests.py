"""
Nose test are defined here.
Usage:
1. Navigate to the projects directory (e.g. ~/loginregister)
2. type nosetest
"""

import os
import re


os.environ['PYTHNONPATH'] = '$PYTHONPATH:$PWD'
os.environ['DJANGO_SETTINGS_MODULE'] = 'loginregister.settings'


from django.test.client import Client
from django.core import mail
from django.test.utils import setup_test_environment
from django.contrib.auth.models import User
from django.db import connection
from loginreg.models import UserProfile


def setup():
    """
    Setuping testing environment. Which includes:
    1. New db creation
    2. Mail outbox creation
    3. Pre-definig data (for registration form)
    """
    os.environ['PYTHNONPATH'] = '$PYTHONPATH:$PWD'
    os.environ['DJANGO_SETTINGS_MODULE'] = 'loginregister.settings'
    setup_test_environment
    connection.creation.create_test_db()


def test_loginsucess():
    """
    Test case, checking that the login function works correctly,
    It sends, a user data which was predefined in setup method, to the
    login handler, and gets response. It uses the status_code
    Which should be 302
    """
    c = Client()
    response = c.post('/login/', {'username': 'oleg', 'password': 'oleg'})
    assert response.status_code == 302, \
        "Login failed, the response code is:%s" %(response.status_code)


def test_incorrect_username():
    """
    Test case which checks if it's possible to login with incorrect
    username. Uses the returned error text presense as a verification point
    """
    c = Client()
    response = c.post('/login/', {'username': 'notoleg', \
                                      'password': 'helland'})
    assert response.content.find("Username or password is incorrect") != -1, \
        "Error code wasn't returned"


def test_incorrect_passw():
    """
    Test case which checks if it's possible to login with incorrect
    password. Uses the returned error text presense as a verification point
    """
    c = Client()
    response = c.post('/login/', {'username': 'notoleg',
                                  'password': 'incorrectPassword'})
    assert response.content.find("Username or password is incorrect") != -1, \
        "Error code wasn't returned"


def test_password_reset_email():
    """
    Test case which checks if it's possible to send a password to a
    user's email, in case it's requested
    """
    c = Client()
    response = c.post('/resend/', {'email': 'oltarasenko@gmail.com'})
    assert response.status_code == 302, "No message was sent"
    assert mail.outbox[0].subject.find("Password reset") != -1,\
        "Message wasn't delivered"


def test_correct_password_was_resent():
    """
    Test case which checks complete process of password reset abilitie
    Changes password of predefined user
    """
    url = re.compile(r'http?://[^ \n ]+')
    c = Client()
    response = c.post('/resend/', {'email': 'oltarasenko@gmail.com'})
    assert response.status_code == 302, "No message was sent"
    assert mail.outbox[0].subject.find("Password reset") != -1, \
        "Message wasn't delivered"
    reset_url = url.search(mail.outbox[0].body).group()
    reset_form = c.post('', {'new_password1': 'olegtame', \
                                 'new_password2': 'olegtame'})
    assert reset_form.content.find("Password reset complete"), \
        "It was impossible to restore passwor"


def test_register():
    """
    Test case which verifies, that it's possible to register a new user
    Checks it using the status code of the response, after the process
    """
    c = Client()
    response = c.post('/register/',
                      {'username': 'newb', 'email': 'example@example.com', \
                           'pass1': 'pass', 'pass2': 'pass'})
    assert response.status_code == 302, \
        "User can't be registered %s" % (response.content)


def test_registerWithBrokenProfile():
    """
    TODO
    Test case checking possibility to register without any profile at all
    I didn't implement the profile completely yet, need more specs to do it
    THE PROFILE ABOUT FIELD IS NOT REQUIERED, so there is no need to check
    if everything will work if it's not passed to the view. e.g.
    FOR NOW I AM CHECKING IF IT"S POSSIBLE TO LOGIN IF YOU DON'T HAVE
    PROFILE
    """
    user = User.objects.create_user(username = 'peter',
                                    password = 'yoyoyo',
                                    email = 'example@ex.com')
    c = Client()
    response = c.post('/login/',
                      {
            'username': 'peter',
            'password': 'yoyoyo'})
    assert response.status_code == 302, \
        "Was impossible to login with user with no profile"


def test_logout():
    """
    Checking if it's possible to logout.
    """
    c = Client()
    response = c.post('/login/', {'username': 'oleg', 'password': 'oleg'})
    logout = c.post('/logout/')
    assert logout.status_code == 302, "Was impossible to logout"


def test_usernameContainsIncorrectCharacters():
    """
    Checking the situation when username has non alphanumeric data
    """
    c = Client()
    response = c.post('/register/',
                      {'username': '__@#$b', 'email': 'exp@example.com',\
                           'pass1': 'pass', 'pass2': 'pass'})
    assert response.content.find("Error") != -1, \
"We submitted user with wrong name"


def test_alreadyTakenUsername():
    """
    Checks if programm handles the situation when user tries
    to register with the username which is already in use by
    another member
    """
    c = Client()
    response = c.post('/register/',
                      {'username': 'oleg', 'email': 'example@example.com',\
                           'pass1': 'pass', 'pass2': 'pass'})
    assert response.content.find("Username is already taken") != -1, \
        "IT became possible to create duplicated user accounts!"
