from django.urls import path
from .views import index, prediction

urlpatterns = [
    path('', index, name='index'),
    path('prediction/', prediction, name='prediction'),
]
