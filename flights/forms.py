from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from flights.models import Airport, Flight, Passenger, Crew


class UserSignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=100, help_text='Required')
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class AirportCreateForm(forms.ModelForm):
	
	class Meta:
		model = Airport
		fields = '__all__'


class AirportUpdateForm(forms.ModelForm):
	
	class Meta:
		model = Airport
		fields = '__all__'


class CrewCreateForm(forms.ModelForm):
	
	class Meta:
		model = Crew
		fields = '__all__'


class CrewUpdateForm(forms.ModelForm):
	
	class Meta:
		model = Crew
		fields = '__all__'



class FlightCreateForm(forms.ModelForm):
	
	class Meta:
		model = Flight
		fields = '__all__'


class FlightUpdateForm(forms.ModelForm):
	
	class Meta:
		model = Flight
		fields = '__all__'


class PassengerCreateForm(forms.ModelForm):
	
	class Meta:
		model = Passenger
		fields = '__all__'
'''		
		fields = [
		'passengerID', 'photo', 'firstName', 'lastName', 'gender', 'email', 'mobile', 
		'country', 'emergencyContact', 'emergencyPhone', 'flights'
		]
'''

class PassengerUpdateForm(forms.ModelForm):
	
	class Meta:
		model = Passenger
		fields = '__all__'