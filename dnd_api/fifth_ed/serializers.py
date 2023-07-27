from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Character


class CharacterSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Character
        fields = [
            "id",
            "name",
            "strength",
            "dexterity",
            "constitution",
            "intelligence",
            "wisdom",
            "charisma",
            "owner",
        ]


class UserSerializer(serializers.ModelSerializer):
    characters = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Character.objects.all()
    )

    class Meta:
        model = User
        fields = ["id", "username", "characters"]
