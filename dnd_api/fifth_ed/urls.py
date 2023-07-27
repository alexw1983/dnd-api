from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from .views import CharacterList, CharacterDetail, UserList, UserDetail

urlpatterns = [
    path("characters/", CharacterList.as_view()),
    path("characters/<int:pk>/", CharacterDetail.as_view()),
    path("users/", UserList.as_view()),
    path("users/<int:pk>/", UserDetail.as_view()),
]
