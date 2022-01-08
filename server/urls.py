from django.contrib import admin
from django.urls import path
from api.views import BookPlaceView, GetBookingsView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/book-place/', BookPlaceView.as_view(), name='book-place'),
    path('api/bookings/<int:pk>/', GetBookingsView.as_view(), name='get-bookings')
]
