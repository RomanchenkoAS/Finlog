from django.shortcuts import render
from django.http import HttpResponse # Render template string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

# Getting local users time
import pytz
from django.utils import timezone
from .models import Category

from accounts.models import User, UserCategory, Entry

import json

from django.utils.timezone import now

# Helper functions
from .helpers import collect_entries, collect_categories


@login_required
def log(request):
    '''Show on the page the list of entries with category classes'''
    current_user = request.user

    categories, user_categories = collect_categories(current_user)
    # print(categories)
    # print(user_categories)
    context = {
        'user': current_user.username,
        'categories': categories,
        'user_categories' : user_categories,
    }

    return render(request, 'log/log.html', context)


@login_required
def load_content(request):
    '''Load entries for log page and pass it as JSON'''
    # Get the list of entries -> transform it to the dictionary for jsonifying
    try:
        # TODO: filter entries by the time period in question 
        t = request.GET.get('t', None)  # Get the value of the 't' parameter
        # All for 'show all entries'
        if t == 'all':
            context = {'entries': collect_entries(request.user)}
        elif t=='month':
            context = {'entries': collect_entries(request.user, filter=t)}
        elif t=='day':
            context = {'entries': collect_entries(request.user, filter=t)}
        else:
            return HttpResponse(status=400)
        
        # Send back JSON
        return JsonResponse(context)
    
    except AttributeError:
        return HttpResponse(status=400)


@csrf_exempt
@login_required
def add(request):
    '''Create a new entry from the form in POST'''
    value = request.POST.get('value', '')
    category = request.POST.get('category', '')
    comment = request.POST.get('comment', '')
    currency = request.user.currency
    
    try:
        category = UserCategory.objects.get(name=category)
    except UserCategory.DoesNotExist:
        # Return error TODO: Make it look ok maybe | apology??
        return HttpResponse(status=400)
    

    # TODO: handle invalid value
    entry = Entry(user=request.user, value=float(value),
                  category=category, comment=comment, date=now(), currency=currency)
    entry.save()

    try:
        # Get the list of entries -> transform it to the dictionary for jsonifying
        entries_dict = {'entries': collect_entries(request.user)}

        # Send back JSON
        return JsonResponse(entries_dict)
    except AttributeError:
        # Return error TODO: Make it look ok maybe | apology??
        return HttpResponse(status=400)


@csrf_exempt
@login_required
def remove(request, p):
    ''' Remove entry #p (p stands for position)'''
    # Calculate the id from given position in the list
    entries_list = collect_entries(request.user)
    
    # Take entry with position p
    entry = entries_list[p]
    # Retrieve id from this dictionary object
    id = entry['id']
    # Get an object with this id
    entry_to_delete = Entry.objects.get(id=id)
    # Finally - delete it
    entry_to_delete.delete()

    # Reload updated list of entries -> transform it to the dictionary for jsonifying
    entries_dict = {'entries': collect_entries(request.user)}

    # Send back JSON
    return JsonResponse(entries_dict)

# TODO : remove csrf exemptions
@csrf_exempt
@login_required
def edit(request):
    # Recieved JSON
    parsed_data = json.loads(request.body)
    # TODO: remove later
    # print(parsed_data)
    
    action = parsed_data['action']
    
    if action == 'edit':
        # Find this one category that needs changing
        category = UserCategory.objects.get(name=parsed_data['name'], user=request.user)
        # Change & save
        category.color = parsed_data['color']
        category.save()
    elif action == 'add':
        # TODO: check if category with this name already exists
        new_category = UserCategory.objects.create(name=parsed_data['newname'], color=parsed_data['color'], user=request.user)
        new_category.save()
        
    elif action == 'delete':
        category = UserCategory.objects.get(name=parsed_data['name'], user=request.user)
        
        default_category = UserCategory.objects.get(name='Other', user=request.user)
        
        entries = Entry.objects.filter(user=request.user, category=category)
        
        for entry in entries:
            entry.category = default_category
            entry.save()
        
        category.delete()
        
    elif action == 'rename':
        category = UserCategory.objects.get(name=parsed_data['name'], user=request.user)
                    
        category.name = parsed_data['newname']
        # Change color as well
        category.color = parsed_data['color']
        category.save()
    
    elif action == 'reset':
        category = UserCategory.objects.get(name=parsed_data['name'], user=request.user)
        # print(category)
        # print(category.name)    
        standard = Category.objects.get(name=category.name)
        category.color = standard.color
        category.save()
    
    # Add error handling || if not 0 - return error message
    # if edit_category(request.user, edit) == 0:
    return HttpResponse(status=204)
    
@csrf_exempt
@login_required
def settings(request):
    # Recieved JSON
    parsed_data = json.loads(request.body)
    # TODO: remove later
    # print(parsed_data)
    
    setting = parsed_data['setting']
    user = User.objects.get(username=request.user.username)
    
    if setting == 'budget':
        new_budget = parsed_data['value']
        user.budget = new_budget
        user.save()
    
    elif setting == 'currency':
        new_currency = parsed_data['value']
        user.currency = new_currency
        user.save()
        
    user_settings = {
        'currency'  : user.currency,
        'budget'    : user.budget,
    }
    
    return JsonResponse(user_settings)