from django.db import models
from encrypted_model_fields.fields import EncryptedTextField

class UserProfile(models.Model):
    username = models.CharField(max_length=150)
    age = models.IntegerField()
    website = models.URLField()
    sensitive_info = EncryptedTextField()