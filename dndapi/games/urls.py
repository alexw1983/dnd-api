from django.urls import path, include

from games import views

urlpatterns = [
    path("characters/", views.CharacterList.as_view()),
    path("characters/<int:character_id>", views.CharacterDetailApiView.as_view()),
]
