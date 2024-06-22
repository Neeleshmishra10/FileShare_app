from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class CustomUser(AbstractUser):
    is_uploader = models.BooleanField(default=False)
    is_downloader = models.BooleanField(default=False)
    is_uploader = models.BooleanField(default=False)  #  Ops Users
    is_client = models.BooleanField(default=False)    #  Client Users
    email_verified = models.BooleanField(default=False)  #  email verification
    
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',  
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',  
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='custom_user'
    )
class File(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    

from django.contrib.auth import get_user_model

User = get_user_model()

class UploadedFile(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.file.name





