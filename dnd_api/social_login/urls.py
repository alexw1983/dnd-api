from django.urls import path

from rest_framework.urlpatterns import format_suffix_patterns
from .views import exchange_token

urlpatterns = [
    # path("exchange/", exchange_token),
    # path(r"exchange/(?P<backend>[^/]+)/$", exchange_token),
    path("exchange/<str:backend>/", exchange_token),
]
