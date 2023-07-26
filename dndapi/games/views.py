from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from .serializers import CharacterSerializer
from .models import Character


def mapRequestToCharacter(request):
    data = {
        "name": request.data.get("name"),
        "level": request.data.get("level"),
        "strength": request.data.get("strength"),
        "dexterity": request.data.get("dexterity"),
        "constitution": request.data.get("constitution"),
        "intelligence": request.data.get("intelligence"),
        "charisma": request.data.get("charisma"),
        "user": request.user.id,
    }

    return data


class CharacterList(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        List all the Character items for given requested user
        """
        todos = Character.objects.filter(user=request.user.id)
        serializer = CharacterSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        """
        Create the Todo with given todo data
        """
        data = mapRequestToCharacter(request)
        serializer = CharacterSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CharacterDetailApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, todo_id, user_id):
        """
        Helper method to get the object with given todo_id, and user_id
        """
        try:
            return Character.objects.get(id=todo_id, user=user_id)
        except Character.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, character_id, *args, **kwargs):
        """
        Retrieves the Character with given Character_id
        """
        todo_instance = self.get_object(character_id, request.user.id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = CharacterSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, character_id, *args, **kwargs):
        """
        Updates the character item with given character_id if exists
        """
        character_instance = self.get_object(character_id, request.user.id)
        if not character_instance:
            return Response(
                {"res": "Object with character id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = mapRequestToCharacter(request)
        serializer = CharacterSerializer(
            instance=character_instance, data=data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, character_id, *args, **kwargs):
        """
        Deletes the todo item with given todo_id if exists
        """
        character_instance = self.get_object(character_id, request.user.id)
        if not character_instance:
            return Response(
                {"res": "Object with character id does not exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        character_instance.delete()

        return Response({"res": "Object deleted!"}, status=status.HTTP_200_OK)
