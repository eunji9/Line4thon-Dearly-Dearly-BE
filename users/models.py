from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nickname = models.CharField(max_length=20, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_letterroom_count = models.IntegerField(default=0)
    sent_letter_count = models.IntegerField(default=0)
    received_letter_count = models.IntegerField(default=0)

