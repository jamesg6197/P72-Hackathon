from django.db import models
from django.contrib.auth.models import User

class ActivityHeatmapData(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    intensity = models.FloatField(help_text="Value to represent the intensity at the point")

    def __str__(self):
        return f"{self.latitude}, {self.longitude}, {self.intensity}"
    
class RegionalDataHeatmap(models.Model):
    region = models.TextField()
    total_activity = models.FloatField()
    #total_profitability = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    

    
class GotoLocationRequest(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    region = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)