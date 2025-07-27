from rest_framework import serializers

class ExportSignalDataSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    latitude = serializers.FloatField()
    longitude = serializers.FloatField()
    rsrp = serializers.FloatField(allow_null=True, required=False)
    rsrq = serializers.FloatField(allow_null=True, required=False)
    rscp = serializers.FloatField(allow_null=True, required=False)
    ecn0 = serializers.FloatField(allow_null=True, required=False)
    rxlev = serializers.FloatField(allow_null=True, required=False)
    cell_id = serializers.IntegerField()
    plmn_id = serializers.CharField()
    node_id = serializers.IntegerField(allow_null=True, required=False)
    tac = serializers.IntegerField(allow_null=True, required=False)
    lac = serializers.IntegerField(allow_null=True, required=False)
    band = serializers.IntegerField(allow_null=True, required=False)
    arfcn = serializers.IntegerField(allow_null=True, required=False)
    scan_tech = serializers.CharField()
