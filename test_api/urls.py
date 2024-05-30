from django.urls import path 

from .views import (
    LoginView,
    RegisterView,
    CarView,
    PlaceView,
    ParkingView
)


urlpatterns = [
    path('login/', LoginView.as_view()),
    path('register/', RegisterView.as_view()),
    path('register/<int:pk>/', RegisterView.as_view()),
    path('car/', CarView.as_view()),
    path('car/<int:pk>/', CarView.as_view()),
    path('place/', PlaceView.as_view()),
    path('place/<int:pk>/', PlaceView.as_view()),
    path('parking/', ParkingView.as_view()),
    path('parking/<int:pk>/', ParkingView.as_view()),
]