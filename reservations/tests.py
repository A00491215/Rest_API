from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Hotel, Reservation, Guest

class HotelReservationTests(APITestCase):
    def setUp(self):
        self.hotel1 = Hotel.objects.create(name="The Grand Halifa", base_price=250.00)
        self.hotel2 = Hotel.objects.create(name="Oceanview Resort", base_price=180.00)

    def test_get_list_of_hotels(self):
        url = reverse('getListOfHotels')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_reservation_confirmation_success(self):
        url = reverse('reservationConfirmation')
        data = {
            "hotel_name": "The Grand Halifa",
            "checkin": "2026-04-10",
            "checkout": "2026-04-15",
            "guests_list": [
                {"guest_name": "John Doe", "gender": "Male"},
                {"guest_name": "Jane Doe", "gender": "Female"}
            ]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('confirmation_number', response.data)
        
        # Verify database
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Guest.objects.count(), 2)

    def test_reservation_overlap(self):
        # Create an initial reservation
        Reservation.objects.create(
            hotel=self.hotel1,
            checkin="2026-04-10",
            checkout="2026-04-15"
        )
        
        url = reverse('reservationConfirmation')
        data = {
            "hotel_name": "The Grand Halifa",
            "checkin": "2026-04-12", # Overlaps
            "checkout": "2026-04-18",
            "guests_list": [{"guest_name": "Alice", "gender": "Female"}]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_get_hotels_filters_overlapping(self):
        # Create an initial reservation
        Reservation.objects.create(
            hotel=self.hotel1,
            checkin="2026-04-10",
            checkout="2026-04-15"
        )
        url = reverse('getListOfHotels')
        response = self.client.get(url, {'checkin': '2026-04-12', 'checkout': '2026-04-18'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Only hotel2 should be returned because hotel1 is booked
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Oceanview Resort")
