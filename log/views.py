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

# Some more fake commits
# And here
# Yoooooo


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
def add_entry(request):
    value = request.POST.get('value', '')
    category = request.POST.get('category', '')
    comment = request.POST.get('comment', '')

    # Not needed
    data = {
        'value': value,
        'category': category,
        'comment': comment,
    }

    print(data)

    category = Category.objects.get(name=category)
    # user = User.objects.get

    entry = Entry(user=request.user, value=float(value), category=category, comment=comment, date=now())
    entry.save()

    # Get the list of entries -> transform it to the dictionary for jsonifying
    entries_dict = {'entries': collect_entries(request.user)}

    # Send back JSON
    return JsonResponse(entries_dict)