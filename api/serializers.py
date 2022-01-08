from django.db.models import fields
from rest_framework.serializers import ModelSerializer
from .models import Booking, Place


class BookingSerializer(ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"


class PlaceSerializer(ModelSerializer):
    class Meta:
        model = Place
        fields = "__all__"
        