from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse # Render string template
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.messages import get_messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from .forms import RegistrationForm, LoginForm

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
            confirmation = form.cleaned_data['confirmation']

            # Validate username and password

            # Creating a user
            user = User.objects.create_user(username, email=None, password=password)
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

# FORM INSIDE DROPDOWN SOMEHOW
# <div class="dropdown-menu">
#   <form class="px-4 py-3">
#     <div class="mb-3">
#       <label for="exampleDropdownFormEmail1" class="form-label">Email address</label>
#       <input type="email" class="form-control" id="exampleDropdownFormEmail1" placeholder="email@example.com">
#     </div>
#     <div class="mb-3">
#       <label for="exampleDropdownFormPassword1" class="form-label">Password</label>
#       <input type="password" class="form-control" id="exampleDropdownFormPassword1" placeholder="Password">
#     </div>
#     <div class="mb-3">
#       <div class="form-check">
#         <input type="checkbox" class="form-check-input" id="dropdownCheck">
#         <label class="form-check-label" for="dropdownCheck">
#           Remember me
#         </label>
#       </div>
#     </div>
#     <button type="submit" class="btn btn-primary">Sign in</button>
#   </form>
#   <div class="dropdown-divider"></div>
#   <a class="dropdown-item" href="#">New around here? Sign up</a>
#   <a class="dropdown-item" href="#">Forgot password?</a>
# </div>