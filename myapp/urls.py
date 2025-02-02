from django.db import router
from django.urls import include, path
from .views import *

urlpatterns = [
    path('passengers/', manage_passenger),
    path('passengers/<int:id>/', manage_passenger),
    path('buses/', manage_bus),
    path('buses/<int:id>/', manage_bus),
    path('routes/', manage_route),
    path('routes/<int:id>/', manage_route),
    path('bookings/', manage_booking),
    path('bookings/<int:id>/', manage_booking),
    path('tickets/', manage_ticket),
    path('tickets/<int:id>/', manage_ticket),
    path('login/', LoginView.as_view()),
    # path('', include(router.urls)),
]


