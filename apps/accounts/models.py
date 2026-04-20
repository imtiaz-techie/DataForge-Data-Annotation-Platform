from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('annotator', 'Annotator'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='annotator')
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def is_admin(self):
        return self.role == 'admin'

    def is_annotator(self):
        return self.role == 'annotator'

    def __str__(self):
        return f"{self.username} ({self.role})"
