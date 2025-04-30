from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.views.decorators.csrf import csrf_exempt
import logging
import json
from .populate import initiate
from .models import CarMake, CarModel
from .restapis import get_request, analyze_review_sentiments, post_review  # Import post_review

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

# View to get the list of dealerships, with optional filtering by state
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    
    dealerships = get_request(endpoint)  # Fetch data using get_request
    if dealerships:
        return JsonResponse({"status": 200, "dealers": dealerships})
    else:
        return JsonResponse({"status": 500, "message": "Failed to fetch dealerships"})

# View to get dealer details by dealer_id
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{str(dealer_id)}"
        dealership = get_request(endpoint)
        if dealership:
            return JsonResponse({"status": 200, "dealer": dealership})
        else:
            logger.error(f"Failed to fetch details for dealer id: {dealer_id}")
            return JsonResponse({"status": 404, "message": "Dealer not found"})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Function to get reviews for a specific dealer and analyze their sentiment
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = f"/fetchReviews/dealer/{str(dealer_id)}"
        reviews = get_request(endpoint)

        if reviews:
            for review_detail in reviews:
                response = analyze_review_sentiments(review_detail['review'])
                if response and 'sentiment' in response:
                    review_detail['sentiment'] = response['sentiment']
                else:
                    review_detail['sentiment'] = 'Unknown'

            return JsonResponse({"status": 200, "reviews": reviews})
        else:
            logger.error(f"No reviews found for dealer id: {dealer_id}")
            return JsonResponse({"status": 404, "message": "No reviews found"})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# View to handle adding a review
def add_review(request):
    if request.method != "POST":
        return JsonResponse({"status": 405, "message": "Method Not Allowed"})
    
    if not request.user.is_anonymous:
        try:
            data = json.loads(request.body)
            response = post_review(data)
            print(response)
            return JsonResponse({"status": 200, "message": "Review posted successfully"})
        except Exception as e:
            logger.error(f"Error in posting review: {str(e)}")
            return JsonResponse({"status": 401, "message": f"Error in posting review: {str(e)}"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})