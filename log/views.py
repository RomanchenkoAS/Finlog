from django.shortcuts import render
from django.http import HttpResponse  # Render template string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Entry, Category

from django.utils.timezone import now

# Helper functions
from .helpers import collect_entries, collect_categories


@login_required
def log(request):
    current_user = request.user

    entries = collect_entries(current_user)
    categories = collect_categories(current_user)

    context = {
        'user'          : current_user.username,
        'entries'       : entries,
        'categories'    : categories,
    }
    return render(request, 'log/log.html', context)

@csrf_exempt
@login_required
def add(request):
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
    # Remove entry #p (stands for position)
    print(f'I am deleting entry #{p}')
    
    # Calculate the id from given position in the list
    entries_list = collect_entries(request.user)
    print('this one:')
    print(entries_list[p])
    
    # Killswitch mwahahaha
    # That's all folks
    pass

    # Get the list of entries -> transform it to the dictionary for jsonifying
    entries_dict = {'entries': collect_entries(request.user)}

    # Send back JSON
    return JsonResponse(entries_dict)
