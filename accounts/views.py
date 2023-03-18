from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse # Render string template
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.models import User # Obsolete
from django.contrib.auth.hashers import make_password, check_password
from .forms import RegistrationForm, LoginForm
from .models import User, UserCategory

def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        # LOGIN PROCESS
        if form.is_valid():
            # Retrieve data from a form
            username, password = form.cleaned_data['username'], form.cleaned_data['password']

            # Find a user with this name
            try:
                user = User.objects.get(username=username)
            except (NameError, User.DoesNotExist):
                # If there is no such user:
                messages.warning(request, f'Authentication failed: user does not exist')
                HttpResponseRedirect('/login')
            else:
                # Check password and authenticate
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    # messages.success(request, f'Authentication successful, {user.username}!')
                    return redirect(reverse('log'))
                else:
                    messages.warning(request, f'Authentication failed: password mismatch')


    elif request.method == 'GET':
        # Render an empty form to pass to the page
        form = LoginForm()

    messages_list = messages.get_messages(request)
    return render(request, 'accounts/login.html', {'messages_list' : messages_list, 'form' : form})

def register(request):

    if request.method == 'POST':
    # For post - actual registration
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # TODO: make proper confirmation  
            confirmation = form.cleaned_data['confirmation']
            budget = form.cleaned_data['budget']
            currency = form.cleaned_data['currency']

            # Validate username and password

            # Creating a user
            user = User.objects.create_user(username, email=None, password=password, budget=budget, currency=currency)
            # At this point user object is already created and saved to the db, user var is not needed
            messages.success(request, f'You have successfully registered, {user.username}!')
            return redirect('accounts:login')

        # If a form is invalid - we render the page with already user pre-populated form
        else:
            messages.info(request, "Form invalid, please try again")

    elif request.method == 'GET':
    # Else -- unbound form
        form = RegistrationForm()

    messages_list = messages.get_messages(request)
    return render(request, 'accounts/register.html', {'messages_list' : messages_list, 'form' : form})



def logout_view(request):
    logout(request)
    messages.info(request, 'You have logged out')
    return HttpResponseRedirect('/login')