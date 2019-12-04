from django.contrib.auth.models import Permission, User
from django.db import models
#from django.urls import reverse


# Create your models here.
class Airport(models.Model):
    airportID = models.CharField(max_length=64, null=True, blank=True)
    name = models.CharField(max_length=164, null=True, blank=True)
    code = models.CharField(max_length=3)
    city = models.CharField(max_length=64)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.city} ({self.code})"


class Aircraft(models.Model):
    aircraftID = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    aircraftType =  models.CharField(max_length=64)
    tailNumber =  models.CharField(max_length=64)
    idealWeight =  models.CharField(max_length=64)
    seatCapacity =  models.CharField(max_length=64)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Status(models.Model):
    name = models.CharField(max_length=64)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Unit(models.Model):
    name = models.CharField(max_length=64)
    location = models.CharField(max_length=64)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Rank(models.Model):
    name = models.CharField(max_length=64)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name}"


class Callsign(models.Model):
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="unitcallsign")
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE, related_name="aircraftcallsign")
    designation = models.CharField(max_length=64)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.designation}"


class Flight(models.Model):
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE, related_name="user")
    flightID = models.CharField(max_length=64)
    callsign = models.ForeignKey(Callsign, on_delete=models.CASCADE, related_name="flightcallsign")
    origin = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="departures")
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name="arrivals")
    aircraft = models.ManyToManyField(Aircraft, related_name="flightaircraft")
    duration = models.IntegerField()
    fuelQty = models.CharField(max_length=64)
    fuelWeight = models.CharField(max_length=64)
    status = models.ForeignKey(Status, on_delete=models.CASCADE, related_name="flightstatus")
    date =  models.DateTimeField(auto_now_add=False)
    eDepartureTime =  models.DateTimeField(auto_now_add=False, null=True, blank=True)
    eArrivalTime =  models.DateTimeField(auto_now_add=False, null=True, blank=True)
    #isDeparted = models.BooleanField()
    #isArrived = models.BooleanField()    
    departureTime =  models.DateTimeField(auto_now_add=False, null=True, blank=True)
    arrivalTime =  models.DateTimeField(auto_now_add=False, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def is_valid_flight(self):
        return (self.origin != self.destination) and (self.duration >= 0)

    def __str__(self):
        return f"{self.flightID} - {self.origin} to {self.destination}"
'''
    # Reverse to flightDetail page using self.pk
    def get_absolute_url(self):
        return reverse('flights:flightDetail', kwargs={'pk': self.pk})
'''

class Passenger(models.Model):    
    photo = models.FileField()
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    gender = models.CharField(max_length=64)
    weight = models.CharField(max_length=64)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=120, null=True, blank=True)
    contactPerson = models.CharField(max_length=64)
    contactPhone = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, related_name="passengers")
    boardingPass = models.CharField(max_length=64)
    seatNumber = models.CharField(max_length=64, null=True, blank=True)
    isLaggage = models.BooleanField()
    laggagePieces = models.CharField(max_length=64, null=True, blank=True)
    laggageTotalWeight = models.CharField(max_length=64, null=True, blank=True)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName} ({self.boardingPass})"


class Crew(models.Model):
    crewID = models.CharField(max_length=64)
    photo = models.FileField()
    firstName = models.CharField(max_length=64)
    lastName = models.CharField(max_length=64)
    gender = models.CharField(max_length=64)
    weight = models.CharField(max_length=64, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, related_name="crewunit")
    rank = models.ForeignKey(Rank, on_delete=models.CASCADE, related_name="crewrank") 
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=64, null=True, blank=True)
    country = models.CharField(max_length=65, null=True, blank=True)
    contactPerson = models.CharField(max_length=64)
    contactPhone = models.CharField(max_length=64)
    flights = models.ManyToManyField(Flight, related_name="crews")
    isLaggage = models.BooleanField()
    laggagePieces = models.CharField(max_length=64, null=True, blank=True)
    laggageTotalWeight = models.CharField(max_length=64, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    timeCreated = models.DateTimeField(auto_now_add=True)
    timeUpdated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName} ({self.rank})"
'''
    def get_absolute_url(self):
        return reverse('flights:pilotDetail', kwargs={'pk': self.pk})
'''