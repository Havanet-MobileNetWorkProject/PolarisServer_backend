from rest_framework import serializers
from .models import *

class PingTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PingTest
        fields = '__all__'
        read_only_fields = ('user',)


class DNSTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = DNSTest
        fields = '__all__'
        read_only_fields = ('user',)


class WebResponseTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebResponseTest
        fields = '__all__'
        read_only_fields = ('user',)


class HTTPUploadTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HTTPUploadTest
        fields = '__all__'
        read_only_fields = ('user',)


class HTTPDownloadTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = HTTPDownloadTest
        fields = '__all__'
        read_only_fields = ('user',)


class SMSTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = SMSTest
        fields = '__all__'
        read_only_fields = ('user',)

