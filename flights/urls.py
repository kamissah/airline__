from django.urls import path
from django.conf.urls import url
from . import views


app_name = 'flights'

urlpatterns = [

    path('', views.index_view, name='index'),
	path('createaccount/', views.usersignup, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate_account, name='activate'),
	path('login/', views.login_user, name='loginUser'),
	path('logout', views.logout_user, name='logoutUser'),

    
	path('flight/create/', views.create_flight, name='flightCreate'),
	path('flightlist/', views.flight_list_view, name='flightList'),
	path('flight_<int:flight_id>/detail/', views.flight_detail_view, name='flightDetail'),
	path('flight_<int:pk>/update/', views.FlightUpdateView.as_view(), name='flightUpdate'),
	#cumRec/flight/pk/delete/
	path('flight_<int:pk>/delete/', views.FlightDeleteView.as_view(), name='flightDelete'),

	path('<int:flight_id>/bookpassenger', views.book_passenger, name='book'),
	path('<int:flight_id>/bookcrew', views.book_crew, name='bookCrew'),

    path('passenger/create/', views.create_passenger, name='passengerCreate'),
	path('passenger_<int:passenger_id>/detail/', views.passenger_detail_view, name='passengerDetail'),
	path('passenger_<int:pk>/update/', views.PassengerUpdateView.as_view(), name='passengerUpdate'),
	#flights/passenger/pk/delete/
	path('passenger_<int:pk>/delete/', views.PassengerDeleteView.as_view(), name='passengerDelete'),

	path('airport/create/', views.create_airport, name='airportCreate'),
	#path('airport_<int:pk>/detail/', views.airport_detail_view, name='airportDetail'),
	#path('airport_<int:pk>/update/', views.airportUpdateView.as_view(), name='airportUpdate'),
	#flights/airport/pk/delete/
	#path('airport_<int:pk>/delete/', views.airportDeleteView.as_view(), name='airportDelete'),

	path('crew/create/', views.create_crew, name='crewCreate'),
	path('crewlist/', views.CrewListView.as_view(), name='crewList'),
	path('crew_<int:pk>/detail/', views.CrewDetailView.as_view(), name='crewDetail'),
	path('crew_<int:pk>/update/', views.CrewUpdateView.as_view(), name='crewUpdate'),
	#cumRec/crew/pk/delete/
	path('crew_<int:crew_id>/delete/', views.CrewDeleteView.as_view(), name='crewDelete'),

]
