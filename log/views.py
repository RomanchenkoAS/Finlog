from django.shortcuts import render
from django.http import HttpResponse # Render template string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# from django.contrib.auth.models import User # Obsolete
from .models import Entry, Category
from accounts.models import User, UserCategory

import json

from django.utils.timezone import now

# Helper functions
from .helpers import collect_entries, collect_categories # collect_user_categories, edit_category


@login_required
def log(request):
    '''Show on the page the list of entries with category classes'''
    current_user = request.user

    categories, user_categories = collect_categories(current_user)
    
    # print("---------------\nInside VIEW: ")
    # print(categories)
    # print(user_categories)
    # user_categories = collect_user_categories(current_user)

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
    entries_dict = {'entries': collect_entries(request.user)}

    # Send back JSON
    return JsonResponse(entries_dict)


@csrf_exempt
@login_required
def add(request):
    '''Create a new entry from the form in POST'''
    value = request.POST.get('value', '')
    category = request.POST.get('category', '')
    comment = request.POST.get('comment', '')

    # print(f'{value} | {category} | {comment}')
    category = Category.objects.get(name=category)

    # TODO: handle invalid value
    entry = Entry(user=request.user, value=float(value),
                  category=category, comment=comment, date=now())
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

@csrf_exempt
@login_required
def edit(request):
    # Recieved JSON
    parsed_data = json.loads(request.body)
    edit = {'name' : parsed_data['name'], 'color' : parsed_data['color']}
    
    # Add error handling || if not 0 - return error message
    # if edit_category(request.user, edit) == 0:
    return HttpResponse(status=204)
    