from django.shortcuts import render
from django.http import HttpResponse  # Render template string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Entry, Category

import json

from django.utils.timezone import now

# Helper functions
from .helpers import collect_entries, collect_categories


@login_required
def log(request):
    '''Show on the page the list of entries with category classes'''
    current_user = request.user

    entries = collect_entries(current_user)
    categories = collect_categories(current_user)

    context = {
        'user'          : current_user.username,
        #'entries'       : entries,
        #'categories'    : categories,
    }
    
    # if it doesnt work just load a page with only user context
    # and make a request from another view to load all else
    # and also write this another view like
    # def load_content(request):
    return render(request, 'log/log.html', context)

@csrf_exempt
@login_required
def add(request):
    '''Create a new entry from the form in POST'''
    value = request.POST.get('value', '')
    category = request.POST.get('category', '')
    comment = request.POST.get('comment', '')

    category = Category.objects.get(name=category)
    # user = User.objects.get

    entry = Entry(user=request.user, value=float(value), category=category, comment=comment, date=now())
    entry.save()

    # Get the list of entries -> transform it to the dictionary for jsonifying
    entries_dict = {'entries': collect_entries(request.user)}

    # Send back JSON
    return JsonResponse(entries_dict)

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
