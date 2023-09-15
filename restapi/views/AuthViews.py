from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from restapi.serializers.UserSerializer import AppUserSerializer, UserSerializer


@api_view(['POST'])
def LoginView(request):
    # generate a docstring for the OPTIONS method

    """
    Login a user

    Authentication Required:
        NO

    Request:
        POST /login
        {
            "email": "",
            "password": ""
        }

    Response:
        200: User logged in successfully
        {
            "token": "token",
            "profile": {
                "id": 1,
                "name": "John Doe",
                "email": "".
                "roles": "ROLE_USER",
                "username": "user",
                "application": 1
            }
        }
        401: Unauthorized
        400: Bad request

    """
    email = request.data.get('email')
    email = email.lower()
    password = request.data.get('password')
    if email is None or password is None:
        return JsonResponse({'error': 'Please provide both email and password'}, status=status.HTTP_400_BAD_REQUEST)
    user = authenticate(request, email=email, password=password)
    print(user)
    if user is not None:
        if user.isUserUser():
            token = Token.objects.get_or_create(user=user)
            print(token[0].key)
            return JsonResponse({
                'token': token[0].key,
                "profile": AppUserSerializer(user).data,
            })
        elif user.isUserSuperAdmin():
            token = Token.objects.get_or_create(user=user)
            print(token[0].key)
            return JsonResponse({
                'token': token[0].key,
                "profile": UserSerializer(user).data,
            })

        else:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        # Return error message or any other response as required
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
