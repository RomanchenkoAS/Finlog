from django.urls import path
from . import views

appname = 'log'
urlpatterns = [
    path('', views.log, name='log'),
    # AJAX requests pathes
    path('add', views.add, name='add'),
    # A support pathes with no view
    path('remove/<int:p>/', views.remove, name='remove'),
    # For loading list of Entries to the page 
    path('load_content/', views.load_content, name='load_content'),
    # Customize category
    path('edit/', views.edit, name='edit'),
]
