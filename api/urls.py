from django.urls import path
from .views import get_token, flattrade_postback

urlpatterns = [
    path("api/get-token/", get_token, name="get_token"),
    path("api/flattrade/postback/", flattrade_postback, name="flattrade_postback"),
]
