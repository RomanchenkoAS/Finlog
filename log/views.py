from django.shortcuts import render
from django.http import HttpResponse  # Same as render template string from Flask
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from .models import Category

from accounts.models import User, UserCategory, Entry

import json

from django.utils.timezone import now

# Helper functions
from .helpers import collect_entries, collect_categories, get_budget, exchange


@login_required
def log(request):
    '''Show on the page the list of entries with category classes'''
    current_user = request.user

    categories, user_categories = collect_categories(current_user)

    budget = get_budget(request.user)
    context = {
        'user': current_user.username,
        'categories': categories,
        'user_categories': user_categories,
        'budget': budget['budget'],
        'spent': budget['spent'],
        'percent': budget['percent'],
        'currency': current_user.currency,
    }

    return render(request, 'log/log.html', context)


@login_required
def load_content(request):
    '''Load entries for log page and pass it as JSON'''
    # Get the list of entries -> transform it to the dictionary for jsonifying
    try:
        # Get the value of the 't' parameter
        t = request.GET.get('t', None)
        # All for 'show all entries'
        if t == 'all':
            context = {'entries': collect_entries(request.user)}
        else:
            context = {'entries': collect_entries(request.user, filter=t)}

        # Send back JSON
        return JsonResponse(context)

    except AttributeError:
        return HttpResponse(status=400)


@csrf_exempt
@login_required
def add(request):
    '''Create a new entry from the form in POST'''
    # If value is not recieved in request, it becomes '' instead of KeyError
    value = request.POST.get('value', '')
    category = request.POST.get('category', 'Other')
    comment = request.POST.get('comment', '')
    currency = request.user.currency

    try:
        category = UserCategory.objects.get(user=request.user, name=category)
    except UserCategory.DoesNotExist:
        # No such category
        return HttpResponse(status=400)

    try:
        entry = Entry(user=request.user, value=float(value),
                  category=category, comment=comment, date=now(), currency=currency)
        entry.save()
    except ValueError:
        # Value not float
        return HttpResponse(status=400)

    try:
        # Get the list of entries -> transform it to the dictionary for jsonifying
        context = {
            'entries': collect_entries(request.user),
            'budget': get_budget(request.user),
        }

        # Send back JSON
        return JsonResponse(context)
    except AttributeError:
        return HttpResponse(status=400)


@csrf_exempt
@login_required
def remove(request, p):
    ''' Remove entry #p (p stands for position)'''
    # Get the value of the 't' parameter
    t = request.GET.get('t', None)
    # All for 'show all entries'
    if t == 'all':
        entries_list = collect_entries(request.user)
    else:
        entries_list = collect_entries(request.user, filter=t)

    # Take entry with position p
    entry = entries_list[p]
    # Retrieve id from this dictionary object
    id = entry['id']
    # Get an object with this id
    entry_to_delete = Entry.objects.get(id=id)
    # Finally - delete it
    entry_to_delete.delete()

    # Reload updated list of entries -> transform it to the dictionary for jsonifying
    context = {
        'entries': collect_entries(request.user),
        'budget': get_budget(request.user),
    }

    # Send back JSON
    return JsonResponse(context)

@csrf_exempt
@login_required
def edit(request):
    # Recieved JSON
    parsed_data = json.loads(request.body)

    print(parsed_data)
    action = parsed_data['action']

    if action == 'edit':
        # Find this one category that needs changing
        category = UserCategory.objects.get(
            name=parsed_data['name'], user=request.user)
        # Change & save
        category.color = parsed_data['color']
        category.save()
    elif action == 'add':
        # Check if name is occupied
        try:
            UserCategory.objects.get(name=parsed_data['newname'], user=request.user)
            # Category already exists, return with code 400
            return HttpResponse(status=400)
        except UserCategory.DoesNotExist:
            # Name is vacant, create category
            new_category = UserCategory.objects.create(
                name=parsed_data['newname'], color=parsed_data['color'], user=request.user)
            new_category.save()

    elif action == 'delete':
        category = UserCategory.objects.get(
            name=parsed_data['name'], user=request.user)

        default_category = UserCategory.objects.get(
            name='Other', user=request.user)

        entries = Entry.objects.filter(user=request.user, category=category)

        for entry in entries:
            entry.category = default_category
            entry.save()

        category.delete()

    elif action == 'rename':
        category = UserCategory.objects.get(
            name=parsed_data['name'], user=request.user)

        category.name = parsed_data['newname']
        # Change color as well
        category.color = parsed_data['color']
        category.save()

    elif action == 'reset':
        category = UserCategory.objects.get(
            name=parsed_data['name'], user=request.user)
        standard = Category.objects.get(name=category.name)
        category.color = standard.color
        category.save()

    return HttpResponse(status=204)


@csrf_exempt
@login_required
def settings(request):
    # Recieved JSON
    parsed_data = json.loads(request.body)

    setting = parsed_data['setting']
    user = User.objects.get(username=request.user.username)

    if setting == 'budget':
        new_budget = parsed_data['value']
        user.budget = new_budget
        user.save()

    elif setting == 'currency':
        new_currency = parsed_data['value']
        # Update budget currency first
        user.budget = exchange(user.budget, user.currency, new_currency)
        # Then change currency for user
        user.currency = new_currency
        user.save()

    budget_info = get_budget(user)

    # Response has the following structure:
    # budget_info = {
    #     'budget'    : budget,
    #     'spent'     : sum,
    #     'currency'  : user.currency,
    #     'percent'   : (sum / budget) * 100,
    # }

    return JsonResponse(budget_info)
