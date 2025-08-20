from django.db import models
from authentication.models import User
class PingTest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="pingtest")
    timestamp = models.DateTimeField()
    ping_response_time = models.FloatField()

class DNSTest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="dnstest")
    timestamp = models.DateTimeField()
    dns_response_time = models.FloatField()

class WebResponseTest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="webresponcetest")
    timestamp = models.DateTimeField()
    web_response_time = models.FloatField()

class HTTPUploadTest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="httpuploadtest")
    timestamp = models.DateTimeField()
    upload_rate = models.FloatField()

class HTTPDownloadTest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="httpdownloadtest")
    timestamp = models.DateTimeField()
    download_rate = models.FloatField()

class SMSTest(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="smstest")
    timestamp_sent = models.DateTimeField()
    timestamp_delivery = models.DateTimeField()
    delivery_duration = models.FloatField()
    message_content = models.TextField()
