from .views import MapDataView ,ExportCSVView , ExportKMLView , ExportJSONView
from django.urls import path

urlpatterns = [
    path("map-data/", MapDataView.as_view(), name="map-data"),
    path("export/csv/", ExportCSVView.as_view(), name="export-csv"),
    path("export/kml/", ExportKMLView.as_view(), name="export-kml"),
    path("export-json/", ExportJSONView.as_view(), name="export-json"),



]
