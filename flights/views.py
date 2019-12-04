from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.decorators import login_required

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
#from django.db.models import Q
from django.urls import reverse
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login, logout

#from .forms import UserSignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
#import simplejson
from .models import Flight, Airport, Passenger, Crew, Aircraft
from .forms import (
    UserSignUpForm,
    AirportCreateForm, 
    AirportUpdateForm,
    FlightCreateForm,
    FlightUpdateForm, 
    PassengerCreateForm,
    PassengerUpdateForm,
    CrewCreateForm,
    CrewUpdateForm,
    )



IMAGE_FILE_TYPES = ['png', 'jpg', 'jpeg']

# Create your views here.

def index_view(request):
    context = {}
    return render(request, "flights/index.html", context)


def create_flight(request):
    if not request.user.is_authenticated:
        return render(request, 'flights/accounts/login.html')
    else:
        form = FlightCreateForm(request.POST or None, request.FILES or None)
        flight = Flight.objects.all()

        if form.is_valid():
            
            for i in flight:
                if i.flightID == form.cleaned_data.get("flightID"):
                    context = {
                        'flight': flight,
                        'form': form,
                        'error_message': 'You already added this flight',
                    }
                    return render(request, 'flights/flight_form.html', context)
            flight = form.save(commit=False)

            flight.user = request.user

            flight.save()
            return render(request, 'flights/flight_list.html', {'flight': flight})
        context = {
            "form": form,
        }
        return render(request, 'flights/flight_form.html', context)


def flight_list_view(request):
    if not request.user.is_authenticated:
        return render(request, 'flights/accounts/login.html')
    context = {
        "flights": Flight.objects.all(),
        'flight_count': Flight.objects.count(),
    }
    return render(request, "flights/flight_list.html", context)


def flight_detail_view(request, flight_id):
    if not request.user.is_authenticated:
        return render(request, 'flights/accounts/login.html')
    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight does not exist")
    flight_passengers = flight.passengers.all()
    flight_crews = flight.crews.all()
    context = {
        "flight": flight,
        #"aircraft": flight.flightaircraft.all(),
        "crews_on_flight": flight.crews.all(),
        "non_crews": Crew.objects.exclude(flights=flight).all(),
        "passengers_on_flight": flight.passengers.all(),
        "non_passengers": Passenger.objects.exclude(flights=flight).all(),
        'flight_passengers': len(flight_passengers),
        'flight_crews': len(flight_crews),
    }
    return render(request, "flights/flight_detail.html", context)


class FlightUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'flights/flight_update_form.html'
    form_class = FlightUpdateForm
    success_url = reverse_lazy('flights:flightList')

    def get_queryset(self):
        return Flight.objects.all()


class FlightDeleteView(LoginRequiredMixin, DeleteView):
    model = Flight
    success_url = reverse_lazy('flights:flightList')


def book_passenger(request, flight_id):
    if not request.user.is_authenticated:
        return render(request, 'flights/accounts/login.html')
    try:
        passenger_id = int(request.POST['passenger'])
        passenger = Passenger.objects.get(pk=passenger_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request, 'flights/error.html', {'message': 'No Selection'})
    except Passenger.FlightNotExist:
        return render(request, 'flights/error.html', {'message': 'No Flight'})
    except Passenger.DoesNotExist:
        return render(request, 'flights/error.html', {'message': 'No Passenger'})

    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse('flights:flightDetail', args=(flight_id,)))


def book_crew(request, flight_id):
    if not request.user.is_authenticated:
        return render(request, 'flights/accounts/login.html')
    try:
        crew_id = int(request.POST['crew'])
        crew = Crew.objects.get(pk=crew_id)
        flight = Flight.objects.get(pk=flight_id)
    except KeyError:
        return render(request, 'flights/error.html', {'message': 'No Selection'})
    except Crew.FlightNotExist:
        return render(request, 'flights/error.html', {'message': 'No Flight'})
    except Crew.DoesNotExist:
        return render(request, 'flights/error.html', {'message': 'No Crew'})

    crew.flights.add(flight)
    return HttpResponseRedirect(reverse('flights:flightDetail', args=(flight_id,)))


''' for authentication and login
---------------------------------------------------------- '''

def logout_user(request):
    logout(request)
    return render(request, "flights/accounts/logout.html", {"message": "Logged out."})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                flight = Flight.objects.filter(user=request.user)
                return render(request, 'flights/index.html', {'flight': flight})
            else:
                return render(request, 'flights/accounts/login.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'flights/accounts/login.html', {'error_message': 'Invalid login'})
    return render(request, 'flights/accounts/login.html')


def usersignup(request):
    if request.method == 'POST':
        form = UserSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('flights/accounts/activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                #'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
    else:
        form = UserSignUpForm()
    return render(request, 'flights/accounts/signup.html', {'form': form})


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')


''' End authentication and login
---------------------------------------------------------- '''

def create_airport(request):
    if not request.user.is_authenticated:
        return render(request, 'flights/accounts/login.html')
    else:
        form = AirportCreateForm(request.POST or None, request.FILES or None)
        airport = Airport.objects.all()
        if form.is_valid():
            
            for r in airport:
                if r.airportID == form.cleaned_data.get("airportID"):
                    context = {
                        'airport': airport,
                        'form': form,
                        'error_message': 'You already added that airport',
                    }
                    return render(request, 'flights/airport_form.html', context)
            airport = form.save(commit=False)

            airport.user = request.user

            airport.save()
            return render(request, 'flights/index.html', {'airport': airport})
        context = {
            "form": form,
        }
        return render(request, 'flights/airport_form.html', context)



def create_passenger(request):
    if not request.user.is_authenticated:
        return render(request, 'flights/accounts/login.html')
    else:
        form = PassengerCreateForm(request.POST or None, request.FILES or None)
        #passenger = get_object_or_404(Passenger, pk=pk)
        passenger = Passenger.objects.all()
        if form.is_valid():
            
            for p in passenger:
                    
                if p.boardingPass == form.cleaned_data.get("boardingPass"):
                    context = {
                        'passenger': passenger,
                        'form': form,
                        'error_message': 'You already added a passenger with this Boarding Pass',
                    }
                    return render(request, 'flights/passenger_form.html', context)
            passenger = form.save(commit=False)

            passenger.user = request.user
            passenger.photo = request.FILES['photo']

            file_type = passenger.photo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'passenger': passenger,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'flights/passenger_form.html', context)
            passenger.save()
            return render(request, 'flights/passenger_detail.html', {'passenger': passenger})
        context = {
            "form": form,
        }
        return render(request, 'flights/passenger_form.html', context)


def passenger_detail_view(request, passenger_id):
    if not request.user.is_authenticated:
        return render(request, 'flights/accounts/login.html')
    try:
        passenger = Passenger.objects.get(pk=passenger_id)
    except Passenger.DoesNotExist:
        raise Http404("Passenger does not exist")
    context = {
        "passenger": passenger,
    }
    return render(request, "flights/passenger_detail.html", context)
    return HttpResponseRedirect(reverse("flight:book", args=(flight_id,)))


class PassengerUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'flights/passenger_update_form.html'
    form_class = PassengerUpdateForm
    success_url = reverse_lazy('flights:flightList')

    def get_queryset(self):
        return Passenger.objects.all()


class PassengerDeleteView(LoginRequiredMixin, DeleteView):
    model = Passenger
    success_url = reverse_lazy('flights:index')


def create_crew(request):
    if not request.user.is_authenticated:
        return render(request, 'flights/accounts/login.html')
    else:
        form = CrewCreateForm(request.POST or None, request.FILES or None)
        #passenger = get_object_or_404(Passenger, pk=pk)
        crew = Crew.objects.all()
        if form.is_valid():
            
            for c in crew:
                    
                if c.crewID == form.cleaned_data.get("crewID"):
                    context = {
                        'crew': crew,
                        'form': form,
                        'error_message': 'You already added that crew',
                    }
                    return render(request, 'flights/crew_form.html', context)
            crew = form.save(commit=False)

            crew.user = request.user
            crew.photo = request.FILES['photo']

            file_type = crew.photo.url.split('.')[-1]
            file_type = file_type.lower()
            if file_type not in IMAGE_FILE_TYPES:
                context = {
                    'crew': crew,
                    'form': form,
                    'error_message': 'Image file must be PNG, JPG, or JPEG',
                }
                return render(request, 'flights/crew_form.html', context)
            crew.save()
            return render(request, 'flights/crew_detail.html', {'crew': crew})
        context = {
            "form": form,
        }
        return render(request, 'flights/crew_form.html', context)


class CrewListView(LoginRequiredMixin, ListView):
    template_name = 'flights/crew_list.html'
    context_object_name = 'crews'

    def get_queryset(self):
        return Crew.objects.all()


class CrewDetailView(LoginRequiredMixin, DetailView):
    model = Crew
    template_name = 'flights/crew_detail.html'
    success_url = reverse_lazy('flights:crewList')
   
    def get_queryset(self):
       return Crew.objects.all()


class CrewUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'flights/crew_update_form.html'
    form_class = CrewUpdateForm
    success_url = reverse_lazy('flights:crewList')

    def get_queryset(self):
        return Crew.objects.all()


class CrewDeleteView(LoginRequiredMixin, DeleteView):
    model = Crew
    success_url = reverse_lazy('flights:crewList')