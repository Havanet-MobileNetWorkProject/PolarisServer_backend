from .views import MapDataView ,ExportCSVView , ExportKMLView
from django.urls import path

urlpatterns = [
    path("map-data/", MapDataView.as_view(), name="map-data"),
    path("export/csv/", ExportCSVView.as_view(), name="export-csv"),
    path("export/kml/", ExportKMLView.as_view(), name="export-kml"),


]
