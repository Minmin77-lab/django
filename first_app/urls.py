from django.urls import path
from .views import attractions, attraction_detail, tickets, users, staff

urlpatterns = [
    path('', attractions, name='attractions'),
    # path('attraction/', attraction, name='attraction'),
    path('tickets/', tickets, name='tickets'),
    path('users/', users, name='users'),
    path('staff/', staff, name='staff'),
    path('attraction/<int:pk>/', attraction_detail, name='attraction_detail'),
]
