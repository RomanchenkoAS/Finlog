from .models import Entry, Category
from django.contrib.auth.models import User


def collect_entries(user):

    # Gather all entries (objects of this class) bound to given user
    entries_list = Entry.objects.filter(user=user.id)

    # Reform this list as a list of dictionaries
    entries_dict = []
    # Enumerate creates a tuple of (i, item) from a single item
    for i, item in enumerate(entries_list):
        new_entry = {
            'value': item.value,
            'currency': item.currency,
            'category': item.category.name,
            'datetime': item.date.strftime("%Y-%m-%d %H:%M:%S %Z"),
            'comment' : item.comment,
            'position': i,
            'id'      : item.id,
        }
        # print(f'Adding an item #{i}: {item.value} / {item.category} / {item.date} || id:{item.id}')
        entries_dict.append(new_entry)

    return entries_dict


def collect_categories(user):

    # Gather all entries (objects of this class) bound to given user
    categories = Category.objects.all()

    # Add user's custom categories to this list:


    return categories

