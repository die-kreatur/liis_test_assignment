from django.core.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from .serializers import BookingSerializer, PlaceSerializer
from .models import Booking, Place


class BookPlaceView(APIView):
    """Бронирование рабочих мест на определенный период"""

    def post(self, request, format=None):
        try:
            date_from = request.data.get('date_from')
            date_to = request.data.get('date_to')
            place = request.data.get('place')

            bookings = Booking.objects.filter(place_id=place)
            query = (
                        Q(date_from__range=[date_from, date_to]) \
                        | Q(date_to__range=[date_from, date_to])
                    ) | (
                        Q(date_from__lte=date_from) \
                        & Q(date_to__gte=date_to)
                    )
            bookings = bookings.filter(query)

            if bookings:
                return Response(
                    {"Error": "The place has been already booked for that dates"},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
                )

            serializer = BookingSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValidationError:
            return Response(
                {"Error": "Invalid data or data format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except ValueError:
            return Response(
                {"Error": "You haven't provided data to post"},
                status=status.HTTP_400_BAD_REQUEST
            )


class GetBookingsView(APIView):
    """Получение актуальных бронирований рабочего места"""
    def get(self, request, pk, format=None):
        try:
            Place.objects.get(id=pk)

            bookings = Booking.objects.filter(place_id=pk)
            serializer = BookingSerializer(bookings, many=True)
            return Response(serializer.data)

        except Place.DoesNotExist:
            return Response(
                {"Error": "There are no bookings because the place with requested id does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )


class FreePlacesView(APIView):
    """Список свободных мест в указанные даты"""
    def get(self, request, date_from, date_to):
        query = (
                    Q(date_from__range=[date_from, date_to]) \
                    | Q(date_to__range=[date_from, date_to])
                ) | (
                    Q(date_from__lte=date_from) \
                    & Q(date_to__gte=date_to)
                )
                        
        bookings = Booking.objects.filter(query)

        places_to_exclude = []
        for booking in bookings:
            places_to_exclude.append(booking.place_id)

        places = Place.objects.exclude(id__in=places_to_exclude)
        serializer = PlaceSerializer(places, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
