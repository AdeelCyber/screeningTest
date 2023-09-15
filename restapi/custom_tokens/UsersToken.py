from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from django.shortcuts import render, HttpResponseRedirect, HttpResponse, redirect
from ..models import *


class UsersToken(TokenAuthentication):
    def authenticate_credentials(self, key):
        model = self.get_model()
        print(key)
        try:
            token = model.objects.select_related('user').get(key=key)
        except model.DoesNotExist:
            raise exceptions.AuthenticationFailed('Invalid token.')

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed('User inactive or deleted.')
        if not token.user.isUserUser():
            raise exceptions.AuthenticationFailed('Not Authorized')
        return (token.user, token)


