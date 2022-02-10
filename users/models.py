from django.contrib.auth.models import AbstractUser
from django.contrib.sessions.models import Session
from django.db import models


class User(AbstractUser):
    ronin = models.ForeignKey('Ronin', on_delete=models.CASCADE)


class Ronin(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name='ronins')
    address = models.CharField(verbose_name='Ronin address', max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
