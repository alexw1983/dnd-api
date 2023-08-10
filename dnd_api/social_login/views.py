from django.conf import settings

from rest_framework import serializers
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from requests.exceptions import HTTPError

from social_django.utils import psa

from google.oauth2 import id_token
from google.auth.transport import requests

from django.contrib.auth.models import User


class SocialSerializer(serializers.Serializer):
    """
    Serializer which accepts an OAuth2 access token.
    """

    access_token = serializers.CharField(
        allow_blank=False,
        trim_whitespace=True,
    )


@api_view(http_method_names=["POST"])
@permission_classes([AllowAny])
@psa()
def exchange_token(request):
    """
    Exchange an OAuth2 access token for one for this site.
    """
    serializer = SocialSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        # set up non-field errors key
        # http://www.django-rest-framework.org/api-guide/exceptions/#exception-handling-in-rest-framework-views
        try:
            nfe = settings.NON_FIELD_ERRORS_KEY
        except AttributeError:
            nfe = "non_field_errors"

        try:
            a_t = serializer.validated_data["access_token"]

            idinfo = id_token.verify_oauth2_token(
                a_t,
                requests.Request(),
                "874396557202-tn6o0ib9vmss70ugki9qco9ihmj5pucg.apps.googleusercontent.com",
            )

            print("================ID INFO==============")
            print(idinfo)
            print("=====================================")

            user = User.objects.filter(email=idinfo["email"])[:1].get()
        except HTTPError as e:
            # An HTTPError bubbled up from the request to the social auth provider.
            # This happens, at least in Google's case, every time you send a malformed
            # or incorrect access key.
            return Response(
                {
                    "errors": {
                        "token": "Invalid token",
                        "detail": str(e),
                    }
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key})
            # if user.is_active:
            #     token, _ = Token.objects.get_or_create(user=user)
            #     return Response({"token": token.key})
            # else:
            #     # user is not active; at some point they deleted their account,
            #     # or were banned by a superuser. They can't just log in with their
            #     # normal credentials anymore, so they can't log in with social
            #     # credentials either.
            #     return Response(
            #         {"errors": {nfe: "This user account is inactive"}},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )
        else:
            # Unfortunately, PSA swallows any information the backend provider
            # generated as to why specifically the authentication failed;
            # this makes it tough to debug except by examining the server logs.

            return Response(
                {"errors": {nfe: "Authentication Failed"}},
                status=status.HTTP_400_BAD_REQUEST,
            )
