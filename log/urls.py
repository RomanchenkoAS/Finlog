from django.urls import path
from . import views

appname = 'log'
urlpatterns = [
    path('', views.log, name='log'),
    # AJAX request path
    path('add', views.add_entry, name='add'),

]
