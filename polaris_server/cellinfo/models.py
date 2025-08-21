from django.db import models

from authentication.models import User

TECHNOLOGY_CHOICES = [
    ('GSM', 'GSM'),
    ('GPRS', 'GPRS'),
    ('EDGE', 'EDGE'),
    ('UMTS', 'UMTS'),
    ('HSPA', 'HSPA'),
    ('HSPA+', 'HSPA+'),
    ('LTE', 'LTE'),
    ('LTE-Adv', 'LTE Advanced'),
    ('5G', '5G'),
]

class BaseSignalTest(models.Model):
    timestamp = models.DateTimeField()
    technology = models.CharField(max_length=20, choices=TECHNOLOGY_CHOICES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    plmn_id = models.CharField(max_length=10)
    cell_id = models.BigIntegerField()
    arfcn = models.IntegerField(null=True, blank=True)
    band = models.IntegerField(null=True, blank=True)

    @property
    def generation(self):
        if self.technology in ['GSM', 'GPRS', 'EDGE']:
            return '2G'
        elif self.technology in ['UMTS', 'HSPA', 'HSPA+']:
            return '3G'
        elif self.technology in ['LTE', 'LTE-Adv']:
            return '4G'
        elif self.technology == '5G':
            return '5G'
        return 'Unknown'


    class Meta:
        abstract = True

class SignalTest2G(BaseSignalTest):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="signal_2g")
    lac = models.IntegerField()
    # rac = models.IntegerField(null=True, blank=True)
    rxlev = models.FloatField(null=True, blank=True)

class SignalTest3G(BaseSignalTest):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="signal_3g")
    lac = models.IntegerField()
    rscp = models.FloatField()
    # ecn0 = models.FloatField(null=True, blank=True)
    node_id = models.BigIntegerField() 


class SignalTest4G(BaseSignalTest):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="signal_4g")
    tac = models.IntegerField()
    rsrp = models.FloatField()
    rsrq = models.FloatField(null=True, blank=True)
    node_id = models.BigIntegerField() 


class SignalTest5G(BaseSignalTest):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="signal_5g")
    tac = models.IntegerField()
    rsrp = models.FloatField()
    rsrq = models.FloatField(null=True, blank=True)
    node_id = models.BigIntegerField() 

