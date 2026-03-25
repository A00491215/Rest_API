import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hotel_reservation.settings')
django.setup()

from reservations.models import Hotel

def populate():
    hotels = [
        {"name": "The Grand Halifa", "base_price": 250.00},
        {"name": "Oceanview Resort", "base_price": 180.00},
        {"name": "Mountain Peak Inn", "base_price": 120.00},
        {"name": "City Center Hotel", "base_price": 300.00},
        {"name": "Historic B&B", "base_price": 90.00}
    ]
    for hotel_data in hotels:
        Hotel.objects.get_or_create(name=hotel_data["name"], defaults={"base_price": hotel_data["base_price"]})
    print("Initial hotels loaded successfully.")

if __name__ == '__main__':
    populate()
