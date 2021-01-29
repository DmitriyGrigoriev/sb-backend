from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
# from rest_framework_simplejwt import serializers, tokens
from .models import  Terminal
from .serializers import TerminalSerializer

# class GetTokenObtainPairSerializer(serializers.TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         return tokens.RefreshToken.for_user(user)
#
#     def validate(self, attrs):
#         data = super().validate(attrs)
#
#         refresh = self.get_token(self.user)
#
#         data['refresh'] = str(refresh)
#         data['access'] = str(refresh.access_token)
#
#         return data
#
#
# class GetTokenObtainPairView(TokenObtainPairView):
#     """
#     Takes a set of user credentials and returns an access and refresh JSON web
#     token pair to prove the authentication of those credentials.
#     """
#     serializer_class = GetTokenObtainPairSerializer


class TerminalView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Terminal.objects.all()

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = TerminalSerializer(queryset, many=True)
        return Response(serializer.data)


class TerminalViewSet(ModelViewSet):
    permission_classes = (IsAuthenticated)
    queryset = Terminal.objects.all()
    serializer_class = TerminalSerializer