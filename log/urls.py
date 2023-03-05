from django.urls import path
from . import views

appname = 'log'
urlpatterns = [
    path('', views.log, name='log'),
    # AJAX requests pathes
    path('add', views.add, name='add'),
    path('remove/<int:p>/', views.remove, name='remove'),
    # A support path with no view || for loading list of Entries to the page 
    path('load_content/', views.load_content, name='load_content'),
]
