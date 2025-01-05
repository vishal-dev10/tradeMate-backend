from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Item
from .serializers import ItemSerializer
import os
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

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
