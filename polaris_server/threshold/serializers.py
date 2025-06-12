from rest_framework import serializers
from .models import ThresholdParameter, ThresholdLevel


class ThresholdLevelInputSerializer(serializers.Serializer):
    level = serializers.IntegerField(min_value=1)
    color = serializers.CharField()
    min = serializers.FloatField()
    max = serializers.FloatField()

class ThresholdParamInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    signal_type = serializers.ChoiceField(choices=["quantity", "quality"])
    levels = ThresholdLevelInputSerializer(many=True)

class UnifiedThresholdInputSerializer(serializers.Serializer):
    technology = serializers.ChoiceField(choices=["2G", "3G", "4G", "5G"])
    parameters = ThresholdParamInputSerializer(many=True)

class ThresholdLevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThresholdLevel
        fields = ['level', 'color', 'min_value', 'max_value']

class ThresholdParameterSerializer(serializers.ModelSerializer):
    levels = ThresholdLevelSerializer(many=True, read_only=True)

    class Meta:
        model = ThresholdParameter
        fields = ['id', 'name', 'technology', 'signal_type', 'levels']
