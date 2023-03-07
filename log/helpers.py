from .models import Entry, Category, UserCategory
from django.contrib.auth.models import User


def collect_entries(user):
    ''' Returns a list of entries for this user '''

    # Gather all entries (objects of this class) bound to given user
    entries_list = Entry.objects.filter(user=user.id)

    # Reform this list as a list of dictionaries
    entries_dict = []
    # Enumerate creates a tuple of (i, item) from a single item
    for i, item in enumerate(entries_list):
        new_entry = {
            'value': item.value,
            'currency': item.currency,
            # To use
            'category': format_name(item.category.name),
            # To show
            'category_title': item.category.name,
            'color': item.category.color,
            'datetime': item.date.strftime("%Y-%m-%d %H:%M:%S %Z"),
            'comment': item.comment,
            'position': i,
            'id': item.id,
        }
        # print(f'Adding an item #{i}: {item.value} / {item.category} / {item.date} || id:{item.id}')
        entries_dict.append(new_entry)

    return entries_dict


def collect_categories(user):
    ''' Returns a list of categories for this user '''
    # Gather all entries (objects of this class) bound to given user
    categories_list = Category.objects.all()

    categories_dict = []

    for category in categories_list:
        new_category = {
            # For display
            'title': category.name,
            # For inner use
            'name': format_name(category.name),
            'id': category.id,
            'color': category.color,
        }
        categories_dict.append(new_category)

    # Add user's custom categories to this list:
    # Lookup user categories
    # Substitute existing categories by user select if they match
    # Otherwise just add them to the list and throw them back

    return categories_dict


def format_name(str):
    ''' Format category name to exclude capital letters / spaces and '-' symbol '''
    str = str.lower()
    str = str.replace(' ', '_')
    str = str.replace('-', '_')
    return str


def edit_category(user, category_to_edit):

    name = category_to_edit['name']
    color = category_to_edit['color']
    
    # Check if default category
    default_categories = Category.objects.all()
    # Or already edited one
    custom_categories = UserCategory.objects.all()

    # This category already exists (modified or not)
    exist = False

    for category in custom_categories:
        if name == category.title():
            exist = True

            # Updating existing custom category
            new_category = UserCategory.objects.get()
            new_category.user = user
            new_category.category = category
            new_category.name = f'{format_name(category.name)}'
            new_category.color = color
            
            new_category.save()
            
            print('updating an existing custom category as follows:')
            print(user)
            print('foreign key : ' + category)
            print('new cat. name' + name)
            print('title: ' + new_category.title())
            print(color)

    # This means: if it is not already in the list of user-edited categories
    if not exist:
        for category in default_categories:
            if name == category.title():
                exist = True

                # Constructing an updated category
                new_category = UserCategory(
                    user=user, category=category, name=f'{format_name(category.name)}', color=color)
                new_category.save()
                
                print('updating an existing custom category as follows:')
                print(user)
                print('foreign key : ' + category)
                print('new cat. name' + name)
                print('title: ' + new_category.title())
                print(color)
            
    # If it is brand-new category
    if not exist:

        print('Ima make a new one')

    return 0
