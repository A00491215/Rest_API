from django.urls import path
from .views import getListOfHotels, reservationConfirmation

urlpatterns = [
    path('getListOfHotels/', getListOfHotels, name='getListOfHotels'),
    path('reservationConfirmation/', reservationConfirmation, name='reservationConfirmation'),
]
