from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views

app_name = "polls"
urlpatterns = [
    # ex: /polls/
    path("", views.IndexView.as_view(), name="index"),
    # ex: /polls/5/
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    # ex: /polls/5/results/
    path("<int:pk>/results/", views.ResultsView.as_view(), name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("multiply/<int:number1>/<int:number2>/", views.multiply, name="multiply"),
    path("storeData", csrf_exempt(views.storeData), name="storeData"),
    path("storeCode", csrf_exempt(views.storeCode), name="storeCode"),
]