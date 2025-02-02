from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from .models import *
from .serializers import *

# Generic API view to handle CRUD operations
def generic_api(model_class, serializer_class):
    @api_view(['GET', 'POST', 'PUT', 'DELETE'])
    def api(request, id=None):
        if request.method == 'GET':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    serializer = serializer_class(instance)
                    return Response(serializer.data)
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'}, status=404)
            else:
                instances = model_class.objects.all()
                serializer = serializer_class(instances, many=True)
                return Response(serializer.data)

        elif request.method == 'POST':
            serializer = serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            return Response(serializer.errors, status=400)

        elif request.method == 'PUT':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    serializer = serializer_class(instance, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response(serializer.data)
                    return Response(serializer.errors, status=400)
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'}, status=404)
            return Response({'message': 'ID is required for update'}, status=400)

        elif request.method == 'DELETE':
            if id:
                try:
                    instance = model_class.objects.get(id=id)
                    instance.delete()
                    return Response({'message': 'Deleted successfully'}, status=204)
                except model_class.DoesNotExist:
                    return Response({'message': 'Object not found'}, status=404)
            return Response({'message': 'ID is required for deletion'}, status=400)

        return Response({'message': 'Invalid method'}, status=405)

    return api


# API views for each entity
manage_passenger = generic_api(Passenger, PassengerSerializer)
manage_bus = generic_api(Bus, BusSerializer)
manage_route = generic_api(Route, RouteSerializer)
manage_booking = generic_api(Booking, BookingSerializer)
manage_ticket = generic_api(Ticket, TicketSerializer)


# Login View for Authentication
class LoginView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Check if the passenger exists
        try:
            passenger = Passenger.objects.get(username=username, password=password)
            return Response({
                "message": "Login successful",
                "passenger_id": passenger.id,
                "name": passenger.full_name
            }, status=status.HTTP_200_OK)
        except Passenger.DoesNotExist:
            return Response({
                "message": "Invalid credentials"
            }, status=status.HTTP_400_BAD_REQUEST)
