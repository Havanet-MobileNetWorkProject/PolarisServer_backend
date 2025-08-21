from django.urls import path
from .views import ThresholdCreateView, ThresholdListView

urlpatterns = [
    path("create/", ThresholdCreateView.as_view(), name="create-thresholds"),
    path("list/", ThresholdListView.as_view(), name="list-thresholds"),
]
