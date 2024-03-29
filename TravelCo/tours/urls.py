from django.urls import path
from . import views


app_name = "tours"

urlpatterns = [
    path("", views.list, name="list"),
    path("<int:tour_id>/", views.detail, name="detail"),
]
