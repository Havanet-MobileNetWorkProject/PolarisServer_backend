from rest_framework import serializers
from .models import *

class PingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PingTest
        fields = '__all__'

class DNSTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DNSTest
        fields = '__all__'

class WebResponseTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebResponseTest
        fields = '__all__'

class HTTPUploadTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HTTPUploadTest
        fields = '__all__'

class HTTPDownloadTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HTTPDownloadTest
        fields = '__all__'

class SMSTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSTest
        fields = '__all__'
