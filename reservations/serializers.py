from rest_framework import serializers
from .models import Hotel, Reservation, Guest

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'base_price']

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['guest_name', 'gender']

class ReservationSerializer(serializers.ModelSerializer):
    guests_list = GuestSerializer(many=True, source='guests')
    hotel_name = serializers.CharField(write_only=True)
    
    class Meta:
        model = Reservation
        fields = ['hotel_name', 'checkin', 'checkout', 'guests_list', 'confirmation_number']
        read_only_fields = ['confirmation_number']

    def create(self, validated_data):
        guests_data = validated_data.pop('guests')
        hotel_name = validated_data.pop('hotel_name')
        
        try:
            hotel = Hotel.objects.get(name__iexact=hotel_name)
        except Hotel.DoesNotExist:
            raise serializers.ValidationError({"hotel_name": f"Hotel '{hotel_name}' does not exist."})
        
        reservation = Reservation.objects.create(hotel=hotel, **validated_data)
        
        for guest_data in guests_data:
            Guest.objects.create(reservation=reservation, **guest_data)
            
        return reservation
