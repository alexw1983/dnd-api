from django.db import models
from django.contrib.auth.models import User


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    level = models.IntegerField()
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()

    def __str__(self):
        return self.name
