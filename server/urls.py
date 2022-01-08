from django.contrib import admin
from django.urls import path
from api.views import BookPlaceView, GetBookingsView, FreePlacesView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/book-place/', BookPlaceView.as_view()),
    path('api/bookings/<int:pk>/', GetBookingsView.as_view()),
    path('api/free-places/<str:date_from>/<str:date_to>', FreePlacesView.as_view())
]
