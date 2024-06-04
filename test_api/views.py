from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth import hashers

import base64

from .models import Parking, Place, User, Car
from .serializers import UserSerializer, ParkingSerializer, PlaceSerializer, CarSerializer
# Create your views here.
# login class 
class LoginView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def post(self, request:Request)->Response:
        # "Authorization": "Basic <base64.encode(username)>:<base64.encode(64)>
        r=request.headers.get("Authorization")
        s=r.split(' ')[1]
        s1=str(base64.b64decode(s))
        username=s1.split(':')[0][2:]
        password=s1.split(':')[1][:-1]
        user=User.objects.filter(username=username)

        if user:
            user = user.first()
            if user.check_password(password):
                return Response('You are successfully logged in!!!', status=status.HTTP_202_ACCEPTED) 
        else:
            return Response("You are not registered in the system or you entered the wrong username!!!", status=status.HTTP_401_UNAUTHORIZED)

# register class
# let the register part work only for the admin user
class RegisterView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    def get(self, request: Request, pk: int = None):
        if pk:
            user = User.objects.get(id=pk)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        else:
            if request.user.is_superuser:
                users = User.objects.all()
                serializer = UserSerializer(users, many=True)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request: Request):
        if request.user.is_superuser:
            data = request.data
            serializer = UserSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# parking class
class ParkingView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    def get(self, request: Request, pk:int = None):
        if pk:
            parking = Parking.objects.get(id=pk)
            serializer = ParkingSerializer(parking)
            return Response(serializer.data)
        elif request.user.is_superuser:
            parkings = Parking.objects.all()
            serializer = ParkingSerializer(parkings, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error':"only superuser can use this function"}, status=status.HTTP_423_LOCKED)
    def post(self, request: Request, pk:int):
        parking = Parking.objects.get(id=pk)
        serializer = ParkingSerializer(parking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# place class
class PlaceView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    def get(self, request: Request, pk:int = None):
        if pk:
            place = Place.objects.get(id=pk)
            serializer = PlaceSerializer(place)
            return Response(serializer.data)
        else:
            if request.user.is_superuser:
                places = Place.objects.all()
                serializer = PlaceSerializer(places, many=True)
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def post(self, request: Request):
        if request.user.is_superuser:
            data = request.data
            serializer = PlaceSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# car class
class CarView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    def get(self, request: Request, pk: int = None):
        if pk:
            car = Car.objects.get(id=pk)
            serializer = CarSerializer(car)
            return Response(serializer.data)
        else:   
            cars = Car.objects.all()
            serializer = CarSerializer(cars, many=True)
            return Response(serializer.data)
        
    def post(self, request: Request):
        data = request.data
        in_out = data.get('in_out')
        car_number = data.get('car_number')
        car = Car.objects.filter(car_number=car_number)
        if car and in_out == 'input':
            # update count add 1 
            car = Car.objects.get(car_number=car_number)
            car.count += 1
            car.save()
            # requests post parking view input 
            return Response({"count": car.count},status=status.HTTP_201_CREATED)
        else:
            serializer = CarSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
        
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
