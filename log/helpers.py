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
    ''' Returns two lists of default/user categories for this user's pk '''
    # Collect default categories
    default_categories_set = Category.objects.all()
    
    # Collect UserCategory objects filtered by current user
    user_categories_set = UserCategory.objects.filter(user=user)
    user_categories_list = []
    for category in user_categories_set:
        user_categories_list.append(category)
    
    # Cycle through default categories and substitute them with according user categories
    for category in default_categories_set:
        # Getting matching item (this is called a list comprehension)
        match = [x for x in user_categories_set if x.name == category.name]
        matching_category = match[0]
        
        # Substitute the existing one with the user edited
        category.color = matching_category.color
        
        # Remove match from user category list
        user_categories_list.remove(matching_category)
        
    # Blank list
    default_categories = []

    # Form a list of dictionaries for default categories (possibly edited)
    for category in default_categories_set:
        new_category = {
            # For display
            'title': category.name,
            # For inner use
            'name': format_name(category.name),
            'id': category.id,
            'color': category.color,
        }
        default_categories.append(new_category)

    # Same as before but for user categories
    user_categories = []

    # Form a list of dictionaries for extra user categories 
    for category in user_categories_list:
        new_category = {
            # For display
            'title': category.name,
            # For inner use
            'name': format_name(category.name),
            'id': category.id,
            'color': category.color,
        }
        user_categories.append(new_category)

    return default_categories, user_categories


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
