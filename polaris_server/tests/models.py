from django.db import models

class PingTest(models.Model):
    client_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    ping_response_time = models.FloatField()

class DNSTest(models.Model):
    client_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    dns_response_time = models.FloatField()

class WebResponseTest(models.Model):
    client_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    web_response_time = models.FloatField()

class HTTPUploadTest(models.Model):
    client_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    upload_rate = models.FloatField()

class HTTPDownloadTest(models.Model):
    client_id = models.CharField(max_length=100)
    timestamp = models.DateTimeField()
    download_rate = models.FloatField()

class SMSTest(models.Model):
    client_id = models.CharField(max_length=100)
    timestamp_sent = models.DateTimeField()
    timestamp_delivery = models.DateTimeField()
    delivery_duration = models.FloatField()
    message_content = models.TextField()
