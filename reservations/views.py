from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .models import Hotel, Reservation
from .serializers import HotelSerializer, ReservationSerializer
from datetime import datetime

@api_view(['GET'])
def getListOfHotels(request):
    checkin = request.query_params.get('checkin')
    checkout = request.query_params.get('checkout')

    hotels = Hotel.objects.all()

    if checkin and checkout:
        try:
            checkin_date = datetime.strptime(checkin, '%Y-%m-%d').date()
            checkout_date = datetime.strptime(checkout, '%Y-%m-%d').date()
            
            if checkin_date >= checkout_date:
                return Response({"error": "Check-out date must be after check-in date."}, status=status.HTTP_400_BAD_REQUEST)
                
            # Find reservations that overlap with the requested dates
            overlapping_reservations = Reservation.objects.filter(
                checkin__lt=checkout_date,
                checkout__gt=checkin_date
            )
            
            # Exclude hotels that are already booked for these dates
            hotels = hotels.exclude(reservations__in=overlapping_reservations)
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = HotelSerializer(hotels, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def reservationConfirmation(request):
    serializer = ReservationSerializer(data=request.data)
    if serializer.is_valid():
        # Additional validation to ensure dates are logical
        checkin_date = serializer.validated_data.get('checkin')
        checkout_date = serializer.validated_data.get('checkout')
        
        if checkin_date >= checkout_date:
             return Response({"error": "Check-out date must be after check-in date."}, status=status.HTTP_400_BAD_REQUEST)
             
        hotel_name = serializer.initial_data.get('hotel_name')
        if not hasattr(serializer, '_validated_data'):
             pass # Serializer handles hotel_name mapping inside create
             
        # Check if the hotel is already booked for these dates
        try:
            hotel = Hotel.objects.get(name__iexact=hotel_name)
            overlapping_reservations = Reservation.objects.filter(
                hotel=hotel,
                checkin__lt=checkout_date,
                checkout__gt=checkin_date
            )
            if overlapping_reservations.exists():
                return Response({"error": "Hotel is not available for these dates."}, status=status.HTTP_400_BAD_REQUEST)
        except Hotel.DoesNotExist:
            pass # Serializer handles this

        reservation = serializer.save()
        return Response(
            {"confirmation_number": reservation.confirmation_number},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
