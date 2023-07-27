from django.db import models


class Character(models.Model):
    owner = models.ForeignKey(
        "auth.User", related_name="characters", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=255)
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    intelligence = models.IntegerField()
    wisdom = models.IntegerField()
    charisma = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
