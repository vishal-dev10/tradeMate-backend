import hashlib
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser

FLATTR_API_URL = "https://authapi.flattrade.in/trade/apitoken"
API_KEY = "f1f4f51b37a3427689cbb4bfbb21785e"
API_SECRET_KEY = "2025.4619d58cebde4fd593b4dbe859b47d5b5f62d3ba8c13bd94"

def generate_api_secret(api_key, request_code, api_secret_key):
    raw_data = api_key + request_code + api_secret_key
    return hashlib.sha256(raw_data.encode()).hexdigest()

@api_view(["POST"])
def get_token(request):
    request_code = request.data.get("request_code")
    client = request.data.get("client")  # Optional for logging

    if not request_code:
        return JsonResponse({"error": "Request code is required"}, status=400)

    api_secret = generate_api_secret(API_KEY, request_code, API_SECRET_KEY)

    payload = {
        "api_key": API_KEY,
        "request_code": request_code,
        "api_secret": api_secret,
    }

    response = requests.post(FLATTR_API_URL, json=payload)
    if response.status_code == 200:
        return JsonResponse(response.json())
    else:
        return JsonResponse({"error": "Failed to fetch token"}, status=response.status_code)

@csrf_exempt
@api_view(["POST"])
def flattrade_postback(request):
    try:
        data = JSONParser().parse(request)  # Parse the JSON payload
        # Example: Log the received event
        print(f"Received postback data: {data}")
        # Process the event (e.g., update database, notify user)
        return JsonResponse({"status": "success"})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
