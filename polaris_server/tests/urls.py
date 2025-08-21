from django.urls import path
from .views import *

urlpatterns = [
    path('ping/', PingTestView.as_view()),
    path('dns/', DNSTestView.as_view()),
    path('web/', WebResponseTestView.as_view()),
    path('http-upload/', HTTPUploadTestView.as_view()),
    path('http-download/', HTTPDownloadTestView.as_view()),
    path('sms/', SMSTestView.as_view()),
]
