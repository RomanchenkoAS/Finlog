from .models import Entry, Category
from accounts.models import User, UserCategory


def collect_entries(user):
    ''' Returns a list of entries for this user'''

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
    ''' Returns a list of user categories for this user's pk '''
    # Collect default categories
    default_categories_list = Category.objects.all()
    
    # For debug
    print('------------------\FIRST WE HAD: ')
    for c in default_categories_list:
        print(f'{c.name} || {c.color}')
    
    # Collect UserCategory objects filtered by current user
    user_categories_list = UserCategory.objects.filter(user=user)
    
    # Cycle through default categories and substitute them with according custom categories
    for index, category in enumerate(default_categories_list):
        print(f'{index}: {category.name} | {category.color} -> users: ', end='')
        
        # Getting according item
        # This is called list comprehension
        custom = [x for x in user_categories_list if x.name == category.name]
        print(f'{custom[0].name} | {custom[0].color}')
        
        # The existing one with the user edited
        category.color = custom[0].color
        # remove from custom cat. list
        
    # For debug
    print('------------------\nAFTER SUBSTITUTION: ')
    for c in default_categories_list:
        print(f'{c.name} || {c.color}')
        
    print('------------------\CUSTOM CATEGORY LIST AFTERWARDS: ')
    for c in user_categories_list:
        print(f'{c.name} || {c.color}')
        
    categories_dict = []

    for category in default_categories_list:
        new_category = {
            # For display
            'title': category.name,
            # For inner use
            'name': format_name(category.name),
            'id': category.id,
            'color': category.color,
        }
        categories_dict.append(new_category)

    return categories_dict

# def collect_user_categories(user):
    ''' Returns a list of categories for this user '''
    # Gather all entries (objects of this class) bound to given user
    categories_list = UserCategory.objects.all()

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

    return categories_dict

def format_name(str):
    ''' Format category name to exclude capital letters / spaces and '-' symbol '''
    str = str.lower()
    str = str.replace(' ', '_')
    str = str.replace('-', '_')
    return str


# def edit_category(user, category_to_edit):

#     name = category_to_edit['name']
#     color = category_to_edit['color']
    
#     # Check if default category
#     default_categories = Category.objects.all()
#     # Or already edited one
#     custom_categories = UserCategory.objects.all()

#     # This category already exists (modified or not)
#     exist = False

#     for category in custom_categories:
#         if name == category.title():
#             exist = True

            
#             # Updating existing custom category
#             new_category = UserCategory.objects.get()
#             new_category.user = user
#             new_category.category = category.category # Get the foreign key 'category' from category variable
#             new_category.name = f'{format_name(category.name)}'
#             new_category.color = color
            
#             new_category.save()
            
#             print('updating an existing custom category as follows:')
#             print(user)
#             print('foreign key : ' )
#             print(category.category)
#             print('new cat. name: ' + name)
#             print('title: ' + new_category.title())
#             print(color)
            

#     # This means: if it is not already in the list of user-edited categories
#     if not exist:
#         for category in default_categories:
#             if name == category.title():
#                 exist = True

#                 # Constructing an updated category
#                 new_category = UserCategory(
#                     user=user, category=category, name=f'{format_name(category.name)}', color=color)
#                 new_category.save()
                
#                 print('updating an existing default category as follows:')
#                 print(user)
#                 print('which one : ' )
#                 print(category)
#                 print('new cat. name: ' + name)
#                 print('title: ' + new_category.title())
#                 print(color)
                

            
#     # TODO: If it is brand-new category
#     if not exist:

#         print('Ima make a new one')

#     return 0
