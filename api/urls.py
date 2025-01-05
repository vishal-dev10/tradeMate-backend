from django.urls import path
from .views import ItemList, FlattradeAuth, FetchHoldings, flattrade_login, fetch_tradebook, flattrade_postback, generate_access_token

urlpatterns = [
    path('items/', ItemList.as_view(), name='item-list'),
    path('flattrade/auth/', FlattradeAuth.as_view(), name='flattrade-auth'),
    path('flattrade/holdings/', FetchHoldings.as_view(), name='flattrade-holdings'),
    path('flattrade/login/', flattrade_login, name='flattrade_login'),
    path('flattrade/generate-token/', generate_access_token, name='generate_access_token'),
    path('flattrade/tradebook/', fetch_tradebook, name='fetch_tradebook'),
    path('flattrade/postback/', flattrade_postback, name='flattrade_postback'),
]
