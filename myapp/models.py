from django.db import models
from django.utils.timezone import now

# Passenger Model
class Passenger(models.Model):
    full_name = models.CharField(max_length=100, default="Unknown")  # Default full name
    username = models.CharField(max_length=50, unique=True,default="username")
    email = models.EmailField(unique=True, default="noemail@example.com")  # Default email
    password = models.CharField(max_length=255,default="1234")
    phone_number = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.full_name


class Route(models.Model):
    route_name = models.CharField(max_length=100)
    starting_point = models.CharField(max_length=100, default="Nugwi")
    end_point = models.CharField(max_length=100)
    distance_km = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)  # Default distance
    estimated_time = models.TimeField(default="00:00:00")  # Default estimated time
    bus_type = models.CharField(max_length=20, choices=[('Luxury', 'Luxury'), ('Standard', 'Standard'), ('Mini', 'Mini')], default='Standard')  # Default bus type
    price_tzs = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Default price

    def __str__(self):
        return f"{self.route_name} ({self.starting_point} - {self.end_point})"

class Bus(models.Model):
    BUS_TYPE_CHOICES = [
        ('Luxury', 'Luxury'),
        ('Standard', 'Standard'),
        ('Mini', 'Mini'),
    ]

    STATUS_CHOICES = [
        ('Available', 'Available'),
        ('Not Available', 'Not Available'),
        ('In Service', 'In Service'),
        ('Under Maintenance', 'Under Maintenance'),
    ]

    bus_number = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=20, choices=BUS_TYPE_CHOICES, default='Standard')  # Default bus type
    capacity = models.PositiveIntegerField(default=50)  # Default capacity
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Available')  # Default bus status
    route = models.ForeignKey(Route, on_delete=models.CASCADE,default="1")  # Foreign key to Route model

    def __str__(self):
        return f"{self.bus_number} ({self.type})"

class Booking(models.Model):
    travel_date = models.DateField()
    travel_time = models.TimeField()
    seat_number = models.IntegerField()
    passenger = models.ForeignKey('Passenger', on_delete=models.CASCADE)
    bus = models.ForeignKey('Bus', on_delete=models.CASCADE)
    route = models.ForeignKey('Route', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        # Automatically assign the next available seat if not provided
        if not self.seat_number:
            # Fetch booked seats for the bus on the same travel date and time
            booked_seats = Booking.objects.filter(
                bus=self.bus,
                travel_date=self.travel_date,
                travel_time=self.travel_time
            ).values_list('seat_number', flat=True)

            # Find the first available seat number from 1 to 45
            available_seat = next(
                (seat for seat in range(1, 46) if seat not in booked_seats), None
            )

            if available_seat is None:
                raise ValueError("No seats available on this bus for the selected date and time.")
            
            self.seat_number = available_seat
        
        super().save(*args, **kwargs)



# Ticket Model
class Ticket(models.Model):
    TICKET_STATUS_CHOICES = [
        ('Booked', 'Booked'),
        ('Cancelled', 'Cancelled'),
    ]

    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, related_name='tickets')
    ticket_number = models.CharField(max_length=20, unique=True)
    seat_number = models.PositiveIntegerField(default=1)  # Default seat number
    passenger_name = models.CharField(max_length=100)
    passenger_email = models.EmailField()
    status = models.CharField(max_length=20, choices=TICKET_STATUS_CHOICES, default='Booked')  # Default status
    booking_date = models.DateTimeField(default=now)  # Default to current datetime

    def __str__(self):
        return f"Ticket {self.ticket_number} - {self.passenger_name}"

