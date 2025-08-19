from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import User
from threshold.models import ThresholdParameter, ThresholdLevel
from threshold.defaults import default_thresholds 

@receiver(post_save, sender=User)
def create_default_thresholds(sender, instance, created, **kwargs):
    if created and instance.role == "user": 
        for tech, params in default_thresholds.items():
            for p in params:
                param = ThresholdParameter.objects.create(
                    user=instance,
                    name=p["name"],
                    technology=tech,
                    signal_type=p["signal_type"],
                )
                for lvl in p["levels"]:
                    ThresholdLevel.objects.create(
                        parameter=param,
                        level=lvl["level"],
                        color=lvl["color"],
                        min_value=lvl["min"],
                        max_value=lvl["max"],
                    )
