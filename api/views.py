from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
import os
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import hashlib

@csrf_exempt
def flattrade_postback(request):
    if request.method == 'POST':
        # Handle the postback data here
        data = request.POST
        # Process the data as needed
        return JsonResponse({'status': 'success'})
    
@csrf_exempt
def flattrade_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        pan_or_dob = request.POST.get('panOrDob')
        response = requests.post(
            f"{settings.FLATTRADE_BASE_URL}/login",
            data={'username': username, 'password': password, 'panOrDob': pan_or_dob}
        )
        return JsonResponse(response.json())

@csrf_exempt
def generate_access_token(request):
    if request.method == 'POST':
        request_code = request.POST.get('request_code')
        api_key = settings.FLATTRADE_API_KEY
        api_secret = settings.FLATTRADE_SECRET_KEY
        hash_value = hashlib.sha256(f"{api_key}{request_code}{api_secret}".encode()).hexdigest()
        response = requests.post(
            f"{settings.FLATTRADE_BASE_URL}/trade/apitoken",
            data={'api_key': api_key, 'request_code': request_code, 'api_secret': hash_value}
        )
        return JsonResponse(response.json())

@csrf_exempt
def fetch_tradebook(request):
    if request.method == 'POST':
        token = request.POST.get('token')
        response = requests.get(
            f"{settings.FLATTRADE_BASE_URL}/tradebook",
            headers={'Authorization': f'Bearer {token}'}
        )
        return JsonResponse(response.json())
    
class FlattradeAuth(APIView):
    def get(self, request):
        """Authenticate and get an access token from Flattrade"""
        url = f"{os.getenv('FLATTRADE_BASE_URL')}/auth/token"
        payload = {
            "client_id": os.getenv("FLATTRADE_CLIENT_ID"),
            "client_secret": os.getenv("FLATTRADE_CLIENT_SECRET"),
            "grant_type": "client_credentials",
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            return Response(response.json())
        return Response({"error": "Failed to authenticate"}, status=response.status_code)
    
class FetchHoldings(APIView):
    def get(self, request):
        """Fetch user holdings from Flattrade"""
        token = request.headers.get("Authorization")
        if not token:
            return Response({"error": "Access token required"}, status=status.HTTP_401_UNAUTHORIZED)

        url = f"{os.getenv('FLATTRADE_BASE_URL')}/holdings"
        response = requests.get(url, headers={"Authorization": f"Bearer {token}"})
        if response.status_code == 200:
            return Response(response.json())
        return Response({"error": "Failed to fetch holdings"}, status=response.status_code)



class ItemList(APIView):
    def get(self, request):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
