from django.db import models  # For basic models management
from django.utils import timezone  # For setting time in DateTimeField
from django.core.validators import MinValueValidator # For setting minimum value in a field
from django.conf import settings  # For using a build-in USER model

import os # For customizing css file at creation of new category

# Default categories
class Category(models.Model):
    '''Describes kinds of spending/income'''

    # Description of the spending/income type
    name = models.CharField(max_length=200)

    # Income or spend
    INCOME = '+'
    SPEND = '-'
    KIND_CHOICES = [
        (INCOME, 'income'),
        (SPEND, 'spend')
    ]

    kind = models.CharField(
        max_length=1,
        choices=KIND_CHOICES,
        default=SPEND,
    )

    color = models.CharField(max_length=7, default='#d3d3d3')

    # Name
    def __str__(self):
        return self.name

    # For proper representation on admin page
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


# List of tuples for currencies
CURRENCY_CHOICES = [
    ('USD', 'US Dollars'),
    ('EUR', 'Euros'),
    ('RUB', 'Russian Rubles'),
    ('KZT', 'Khazakh Tenge')
    # Add more here..
]


class Entry(models.Model):
    # Using built-in user model <3
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # By default the category is "other"
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=3, default='KZT')
    value = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=200, blank=True)

    # For proper representation on admin page
    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"

    # Name of the entry
    def __str__(self):
        username = self.user.get_username()
        name = f'{username}:{self.category}:{self.value:2.0f}{self.currency}'
        return name
