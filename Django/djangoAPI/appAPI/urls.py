from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

urlpatterns = [
    path("storeData", csrf_exempt(views.storeData), name="storeData"),
    path("storeCode", csrf_exempt(views.storeCode), name="storeCode"),
]