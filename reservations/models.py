from django.db import models
import uuid

class Hotel(models.Model):
    name = models.CharField(max_length=255)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)

    def __str__(self):
        return self.name

class Reservation(models.Model):
    confirmation_number = models.CharField(max_length=100, unique=True, default=uuid.uuid4)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='reservations')
    checkin = models.DateField()
    checkout = models.DateField()

    def __str__(self):
        return f"Reservation {self.confirmation_number} at {self.hotel.name}"

class Guest(models.Model):
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='guests')
    guest_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=50)

    def __str__(self):
        return self.guest_name
