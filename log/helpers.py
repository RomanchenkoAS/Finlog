from .models import Category
from accounts.models import UserCategory, Entry


def collect_entries(user, filter='all'):
    ''' Returns a list of entries for this user'''

    # Gather all entries (objects of this class) bound to given user
    if filter == 'all':
        entries_list = Entry.objects.filter(user=user.id)

    elif filter == 'day':
        entries_list = Entry.filter_today(user)

    elif filter == 'month':
        entries_list = Entry.filter_month(user)

    # Reform this list as a list of dictionaries
    entries_dict = []
    # Enumerate creates a tuple of (i, item) from a single item
    for i, item in enumerate(entries_list):

        new_entry = {
            'value': item.value,
            'currency': item.currency,
            'category': item.category.name,
            'color': UserCategory.objects.get(name=item.category.name, user=user).color,
            'datetime': item.date.strftime("%Y-%m-%d %H:%M:%S %Z"),
            'comment': item.comment,
            'position': i,
            'id': item.id,
        }
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
            'name': category.name,
            'id': category.id,
            'color': category.color,
            'info': info(category.name.lower()),
        }
        default_categories.append(new_category)

    # Same as before but for user categories
    user_categories = []

    # Form a list of dictionaries for extra user categories
    for category in user_categories_list:
        new_category = {
            'name': category.name,
            'id': category.id,
            'color': category.color,
        }
        user_categories.append(new_category)

    return default_categories, user_categories


def exchange(val, currency, target='USD'):
    '''exchange(val, currency) changes to USD || exchange(val,currency,target) changes to Target currency'''
    rate = {
        'KZT': 0.0022,
        'EUR': 1.06,
        'RUB': 0.013,
        'USD': 1,
    }

    usd = val * rate[currency]
    if target == "USD":
        return usd

    else:
        return usd / rate[target]


def get_budget(user):
    """Counts users expences for last month and give back result in user currency"""
    budget = float(user.budget)

    monthly_entries = collect_entries(user, 'month')

    sum = 0
    for entry in monthly_entries:
        sum += exchange(entry['value'], entry['currency'], user.currency)

    budget_info = {
        'budget': budget,
        'spent': sum,
        'currency': user.currency,
        'percent': (sum / budget) * 100,
    }

    return budget_info


def info(category):
    descriptions = {
        'other': 'Anything that does not fit in any other category',
        'housing': 'Rent/mortgage payments, property taxes, home insurance, and utilities',
        'transportation': 'Car payments, gas, insurance, and maintenance costs',
        'food': 'Groceries, dining out, snacks, beverages',
        'entertainment': 'Movies, concerts, hobbies, vacations, subscriptions, books',
        'health': 'Doctor visits, prescriptions, dental care, vision care',
        'savings': 'Emergency fund, retirement savings, investment accounts',
    }

    return descriptions[category]
