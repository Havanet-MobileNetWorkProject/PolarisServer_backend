from django.urls import path
from .views import UnifiedSignalTestView

urlpatterns = [
    path('signal/', UnifiedSignalTestView.as_view()),
]
