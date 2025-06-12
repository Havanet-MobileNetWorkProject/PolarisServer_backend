from .views import MapDataView
from django.urls import path

urlpatterns = [
    path("map-data/", MapDataView.as_view(), name="map-data"),
]
