from rest_framework import serializers
from .models import SignalTest2G, SignalTest3G, SignalTest4G, SignalTest5G

class SignalTest2GSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalTest2G
        fields = '__all__'

class SignalTest3GSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalTest3G
        fields = '__all__'

class SignalTest4GSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalTest4G
        fields = '__all__'

class SignalTest5GSerializer(serializers.ModelSerializer):
    class Meta:
        model = SignalTest5G
        fields = '__all__'
