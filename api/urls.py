from django.urls import path
from .views import ItemList,FlattradeAuth, FetchHoldings

urlpatterns = [
    path('items/', ItemList.as_view(), name='item-list'),
    path('flattrade/auth/', FlattradeAuth.as_view(), name='flattrade-auth'),
    path('flattrade/holdings/', FetchHoldings.as_view(), name='flattrade-holdings'),
]
