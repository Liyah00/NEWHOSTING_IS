from rest_framework import serializers
from .models import Passenger, Bus, Route, Booking, Ticket

# Passenger Serializer
class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = '__all__'

# Bus Serializer
class BusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bus
        fields = '__all__'

# Route Serializer
class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = '__all__'

# Booking Serializer
class BookingSerializer(serializers.ModelSerializer):
    passenger = serializers.SlugRelatedField(slug_field="full_name", queryset=Passenger.objects.all())
    bus = serializers.SlugRelatedField(slug_field="bus_number", queryset=Bus.objects.all())
    route = serializers.SlugRelatedField(slug_field="route_name", queryset=Route.objects.all())
    class Meta:
        model = Booking
        fields = '__all__'

# Ticket Serializer
class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = '__all__'
