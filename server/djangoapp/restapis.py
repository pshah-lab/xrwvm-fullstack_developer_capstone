import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base URLs for backend and sentiment analyzer service
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

def get_request(endpoint, **kwargs):
    # Build URL with optional query parameters
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += f"{key}={value}&"
        params = params.rstrip("&")  # Remove trailing ampersand

    # Construct the full request URL
    request_url = f"{backend_url}{endpoint}?{params}" if params else f"{backend_url}{endpoint}"

    print(f"GET from {request_url}")
    try:
        # Call GET method of requests library with URL and parameters
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return None

def analyze_review_sentiments(text):
    # Construct the URL for sentiment analysis
    request_url = f"{sentiment_analyzer_url}analyze/{text}"
    try:
        # Call GET method of requests library for sentiment analysis
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return None

# Function to get a list of all dealerships or dealerships by state
def get_dealerships(state="All"):
    # If state is provided, use it to fetch specific dealerships
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    
    # Call get_request function to fetch dealership data
    dealerships = get_request(endpoint)
    return dealerships

# Function to get details of a specific dealer by dealer_id
def get_dealer_details(dealer_id):
    if dealer_id:
        endpoint = f"/fetchDealer/{dealer_id}"
        # Call get_request function to fetch specific dealer's details
        dealer_details = get_request(endpoint)
        return dealer_details
    else:
        print("Invalid dealer_id provided.")
        return None


# Method to post a review to the backend
def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        # Make the POST request to the backend with the provided data
        response = requests.post(request_url, json=data_dict)
        
        # Print the response for debugging purposes
        print(response.json())
        
        # Return the response from the backend (this can be a success message or error)
        return response.json()
    except Exception as e:
        print(f"Network exception occurred: {e}")
        return {"status": "error", "message": str(e)}        