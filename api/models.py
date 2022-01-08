from django.db import models


class Place(models.Model):
    """Place model"""
    number = models.IntegerField(unique=True)

    def __str__(self):
        return f"Place {self.number}"


class Booking(models.Model):
    """Model for booking places"""
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    date_from = models.DateField()
    date_to = models.DateField()

    def __str__(self):
        return f"Booking of {self.place.number} {self.date_from} - {self.date_to}"
