from django.urls import path
from .views import UnifiedSignalTestView

urlpatterns = [
    path('tests/signal/', UnifiedSignalTestView.as_view()),
]
