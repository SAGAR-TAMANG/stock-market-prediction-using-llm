from django.urls import path
from .views import index, prediction, stock_chart_view

urlpatterns = [
    path('', index, name='index'),
    path('prediction/', prediction, name='prediction'),
    path('stock_chart_view/', stock_chart_view, name='stock_chart_view'),
]
