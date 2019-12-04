from django.contrib import admin

from .models import Airport, Flight, Passenger, Crew, Callsign, Aircraft, Unit, Status, Rank

# Register your models here.

class PassengerInline(admin.StackedInline):
    model = Passenger.flights.through
    extra = 1

class FlightAdmin(admin.ModelAdmin):
    inlines = [PassengerInline]

class PassengerAdmin(admin.ModelAdmin):
    filter_horizontal = ("flights",)

admin.site.register(Airport)
admin.site.register(Crew)
admin.site.register(Flight, FlightAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Callsign)
admin.site.register(Aircraft)
admin.site.register(Unit)
admin.site.register(Status)
admin.site.register(Rank)
