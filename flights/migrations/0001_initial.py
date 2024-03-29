# Generated by Django 2.2.6 on 2019-12-03 19:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('aircraftID', models.CharField(max_length=64)),
                ('name', models.CharField(max_length=64)),
                ('aircraftType', models.CharField(max_length=64)),
                ('tailNumber', models.CharField(max_length=64)),
                ('idealWeight', models.CharField(max_length=64)),
                ('seatCapacity', models.CharField(max_length=64)),
                ('timeCreated', models.DateTimeField(auto_now_add=True)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('airportID', models.CharField(blank=True, max_length=64, null=True)),
                ('name', models.CharField(blank=True, max_length=164, null=True)),
                ('code', models.CharField(max_length=3)),
                ('city', models.CharField(max_length=64)),
                ('timeCreated', models.DateTimeField(auto_now_add=True)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Callsign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('designation', models.CharField(max_length=64)),
                ('timeCreated', models.DateTimeField(auto_now_add=True)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
                ('aircraft', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='aircraftcallsign', to='flights.Aircraft')),
            ],
        ),
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flightID', models.CharField(max_length=64)),
                ('duration', models.IntegerField()),
                ('fuelQty', models.CharField(max_length=64)),
                ('fuelWeight', models.CharField(max_length=64)),
                ('date', models.DateTimeField()),
                ('eDepartureTime', models.DateTimeField(blank=True, null=True)),
                ('eArrivalTime', models.DateTimeField(blank=True, null=True)),
                ('departureTime', models.DateTimeField(blank=True, null=True)),
                ('arrivalTime', models.DateTimeField(blank=True, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('timeCreated', models.DateTimeField(auto_now_add=True)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
                ('aircraft', models.ManyToManyField(related_name='flightaircraft', to='flights.Aircraft')),
                ('callsign', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flightcallsign', to='flights.Callsign')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='flights.Airport')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departures', to='flights.Airport')),
            ],
        ),
        migrations.CreateModel(
            name='Rank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('timeCreated', models.DateTimeField(auto_now_add=True)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('timeCreated', models.DateTimeField(auto_now_add=True)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('location', models.CharField(max_length=64)),
                ('timeCreated', models.DateTimeField(auto_now_add=True)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.FileField(upload_to='')),
                ('firstName', models.CharField(max_length=64)),
                ('lastName', models.CharField(max_length=64)),
                ('gender', models.CharField(max_length=64)),
                ('weight', models.CharField(max_length=64)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=64, null=True)),
                ('country', models.CharField(blank=True, max_length=120, null=True)),
                ('contactPerson', models.CharField(max_length=64)),
                ('contactPhone', models.CharField(max_length=64)),
                ('boardingPass', models.CharField(max_length=64)),
                ('seatNumber', models.CharField(blank=True, max_length=64, null=True)),
                ('isLaggage', models.BooleanField()),
                ('laggagePieces', models.CharField(blank=True, max_length=64, null=True)),
                ('laggageTotalWeight', models.CharField(blank=True, max_length=64, null=True)),
                ('timeCreated', models.DateTimeField(auto_now_add=True)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
                ('flights', models.ManyToManyField(related_name='passengers', to='flights.Flight')),
            ],
        ),
        migrations.AddField(
            model_name='flight',
            name='status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flightstatus', to='flights.Status'),
        ),
        migrations.AddField(
            model_name='flight',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Crew',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('crewID', models.CharField(max_length=64)),
                ('photo', models.FileField(upload_to='')),
                ('firstName', models.CharField(max_length=64)),
                ('lastName', models.CharField(max_length=64)),
                ('gender', models.CharField(max_length=64)),
                ('weight', models.CharField(blank=True, max_length=64, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=64, null=True)),
                ('country', models.CharField(blank=True, max_length=65, null=True)),
                ('contactPerson', models.CharField(max_length=64)),
                ('contactPhone', models.CharField(max_length=64)),
                ('isLaggage', models.BooleanField()),
                ('laggagePieces', models.CharField(blank=True, max_length=64, null=True)),
                ('laggageTotalWeight', models.CharField(blank=True, max_length=64, null=True)),
                ('remarks', models.TextField(blank=True, null=True)),
                ('timeCreated', models.DateTimeField(auto_now_add=True)),
                ('timeUpdated', models.DateTimeField(auto_now=True)),
                ('flights', models.ManyToManyField(related_name='crews', to='flights.Flight')),
                ('rank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crewrank', to='flights.Rank')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crewunit', to='flights.Unit')),
            ],
        ),
        migrations.AddField(
            model_name='callsign',
            name='unit',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='unitcallsign', to='flights.Unit'),
        ),
    ]
