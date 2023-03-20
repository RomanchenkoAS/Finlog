from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RegistrationForm, LoginForm
from .models import User

def login_view(request):

    if request.method == 'POST':
        form = LoginForm(request.POST)
        # Login process
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
            budget = form.cleaned_data['budget']
            currency = form.cleaned_data['currency']
            
            # Creating a user
            user = User.objects.create_user(username, email=None, password=password, budget=budget, currency=currency)
            
            messages.success(request, f'You have successfully registered, {user.username}! Use your login & password to enter.')
            return redirect('accounts:login')
            
    # An unbound form if user visits for the first time
    elif request.method == 'GET':
        form = RegistrationForm()

    messages_list = messages.get_messages(request)
    return render(request, 'accounts/register.html', {'messages_list' : messages_list, 'form' : form})



def logout_view(request):
    logout(request)
    messages.info(request, 'You have logged out')
    return HttpResponseRedirect('/login')