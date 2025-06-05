from django.db import models

class BaseSignalTest(models.Model):
    client_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    generation = models.CharField(max_length=3, choices=[
        ('2G', '2G'),
        ('3G', '3G'),
        ('4G', '4G'),
        ('5G', '5G'),
    ])
    latitude = models.FloatField()
    longitude = models.FloatField()
    plmn_id = models.CharField(max_length=10)
    cell_id = models.BigIntegerField()
    
    class Meta:
        abstract = True

class SignalTest2G(BaseSignalTest):
    rxlev = models.FloatField()
    lac = models.IntegerField()
    arfcn = models.IntegerField(null=True, blank=True)
    band = models.IntegerField(null=True, blank=True)

class SignalTest3G(BaseSignalTest):
    rscp = models.FloatField()
    ecn0 = models.FloatField()
    lac = models.IntegerField()
    arfcn = models.IntegerField(null=True, blank=True)
    band = models.IntegerField(null=True, blank=True)

class SignalTest4G(BaseSignalTest):
    rsrp = models.FloatField()
    rsrq = models.FloatField()
    tac = models.IntegerField()
    arfcn = models.IntegerField(null=True, blank=True)
    band = models.IntegerField(null=True, blank=True)

class SignalTest5G(BaseSignalTest):
    rsrp = models.FloatField()
    rsrq = models.FloatField()
    tac = models.IntegerField()
    arfcn = models.IntegerField(null=True, blank=True)
    band = models.IntegerField(null=True, blank=True)
