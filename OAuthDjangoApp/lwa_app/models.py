from django.db import models
from django.contrib.auth.models import User


class AmazonSPAPIConnection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="amazon_spapi_connections")
    refresh_token = models.CharField(max_length=600, default="")
