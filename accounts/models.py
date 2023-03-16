from django.db import models
from django.contrib.auth.models import AbstractUser
from log.models import Category
from django.conf import settings  # For using a build-in USER model
from django.utils import timezone  # For setting time in DateTimeField
from django.db.models.functions import TruncMonth, TruncDay

# For setting minimum value in a field
from django.core.validators import MinValueValidator

# List of tuples for currencies
CURRENCY_CHOICES = [
    ('USD', 'US Dollars'),
    ('EUR', 'Euros'),
    ('RUB', 'Russian Rubles'),
    ('KZT', 'Khazakh Tenge'),
    # Add more here if needed
]

# Custom user model containing a list of categories and according methods
class User(AbstractUser):
    
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, default='KZT')
    
    budget = models.FloatField(default = 0)
    
    def generate_categories(self):
        # Add all the default categories to the user
        list = Category.objects.all()
        
        for item in list:
            UserCategory.objects.create(name=item.name, color=item.color, user=self)

    def get_user_categories(self):
        return UserCategory.objects.filter(user=self)

    def add_user_category(self, name, color):
        user_category = UserCategory.objects.create(name=name, color=color, user=self)
        return user_category

    def remove_user_category(self, user_category):
        user_category.delete()
        
    def save(self, *args, **kwargs):
        # Check if this is a new user - he has no primary key
        is_new = not self.pk  
        super().save(*args, **kwargs)
        if is_new:
            # Actually generate default categories list
            self.generate_categories()
    
class UserCategory(models.Model):
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=7, default='#d3d3d3')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    # For proper representation on admin page
    class Meta:
        verbose_name = "User category"
        verbose_name_plural = "User categories"
        
    # Name of the entry
    def __str__(self):
        username = self.user.username
        title = f'{self.name} edited by {username}'
        return title
    
class Entry(models.Model):
    # Using built-in user model <3
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    
    # TODO on delete - default
    category = models.ForeignKey(UserCategory, on_delete=models.CASCADE, null=True, blank=True)
    
    
    currency = models.CharField(
        choices=CURRENCY_CHOICES, max_length=3, default='KZT')
    value = models.FloatField(validators=[MinValueValidator(0)])
    date = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=200, blank=True)

    def filter_today(user):
        today = timezone.now().date()

        # Get entries for today
        entries_list = Entry.objects.filter(
            user=user,
            date__date=today  # Today's date
        )

        return entries_list


    def filter_month(user):
        today = timezone.now().date()
        month = today.month
        year = today.year

        # Get entries for this month
        entries_list = Entry.objects.filter(
            user=user,
            date__month=month,  # This month's number
            date__year=year  # This year's number
        )

        return entries_list


    # For proper representation on admin page
    class Meta:
        verbose_name = "Entry"
        verbose_name_plural = "Entries"

    # Name of the entry
    def __str__(self):
        username = self.user.get_username()
        name = f'{username}:{self.category}:{self.value:2.0f}{self.currency}'
        return name
