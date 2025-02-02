from django.contrib import admin
from .models import Booking, Bus, Route, Passenger, Ticket

admin.site.register(Bus)
admin.site.register(Route)
admin.site.register(Passenger)
admin.site.register(Ticket)
admin.site.register(Booking)