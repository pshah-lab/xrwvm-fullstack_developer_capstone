from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import logging
import json
from .populate import initiate

from .models import CarMake, CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data.get('userName')
            password = data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({"userName": username, "status": "Authenticated"})
            else:
                return JsonResponse({"userName": username, "status": "Invalid credentials"}, status=401)
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return JsonResponse({"status": "Error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "Invalid request method"}, status=405)

@csrf_exempt
def logout_user(request):
    if request.method == "POST":
        try:
            logout(request)
            return JsonResponse({"userName": "", "status": "Logged out"})
        except Exception as e:
            logger.error(f"Error during logout: {e}")
            return JsonResponse({"status": "Error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "Invalid request method"}, status=405)

@csrf_exempt
def registration(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            username = data['userName']
            password = data['password']
            first_name = data['firstName']
            last_name = data['lastName']
            email = data['email']

            if User.objects.filter(username=username).exists():
                return JsonResponse({"userName": username, "error": "Already Registered"}, status=409)

            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            login(request, user)
            return JsonResponse({"userName": username, "status": "Authenticated"})
        except Exception as e:
            logger.error(f"Error during registration: {e}")
            return JsonResponse({"status": "Error", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "Invalid request method"}, status=405)

# View to get the list of cars
def get_cars(request):
    try:
        if CarMake.objects.count() == 0:
            initiate()  # Make sure this function exists and is defined properly

        car_models = CarModel.objects.select_related('car_make')
        cars = [{"CarModel": cm.name, "CarMake": cm.car_make.name} for cm in car_models]
        return JsonResponse({"CarModels": cars})
    except Exception as e:
        logger.error(f"Error fetching cars: {e}")
        return JsonResponse({"status": "Error", "message": str(e)}, status=500)