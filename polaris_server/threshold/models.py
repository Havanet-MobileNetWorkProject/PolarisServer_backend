from django.db import models
from authentication.models import User

class ThresholdParameter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="thresholds")

    name = models.CharField(max_length=20)
    technology = models.CharField(max_length=10, choices=[
        ('2G', '2G'), ('3G', '3G'), ('4G', '4G'), ('5G', '5G')
    ])
    signal_type = models.CharField(max_length=10, choices=[
        ('quantity', 'Quantity'),
        ('quality', 'Quality')
    ])
    def __str__(self):
        return f"User {self.user.id} | {self.technology} - {self.name} ({self.signal_type})"

class ThresholdLevel(models.Model):
    parameter = models.ForeignKey(ThresholdParameter, on_delete=models.CASCADE, related_name='levels')
    level = models.PositiveSmallIntegerField()
    color = models.CharField(max_length=20)
    min_value = models.FloatField()
    max_value = models.FloatField()

    class Meta:
        ordering = ['level']
        unique_together = ('parameter', 'level')

    def __str__(self):
        return f"{self.parameter.name} | Level {self.level}"
