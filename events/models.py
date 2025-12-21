from django.db import models
from django.conf import settings
import secrets

# Create your models here.
class Event(models.Model):
    channel = models.CharField(max_length=100)
    sequence_id= models.BigIntegerField()
    timestamp= models.DateTimeField(auto_now_add=True)
    payload=models.JSONField()

    class Meta:
        indexes = [
            models.Index(fields=['channel','sequence_id'])
        ]
        unique_together= ('channel','sequence_id')

    def __str__(self): 
        return f'{self.channel}#{self.sequence_id}'  
    

class AccessToken(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="access_token"
    )
    key = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate():
        return secrets.token_hex(32)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Token for {self.user.id}"