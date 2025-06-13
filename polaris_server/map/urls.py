from .views import MapDataView ,ExportCSVView
from django.urls import path

urlpatterns = [
    path("map-data/", MapDataView.as_view(), name="map-data"),
    path("export/csv/", ExportCSVView.as_view(), name="export-csv"),
]
