from rest_framework import generics, status

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from restapi.custom_tokens.UsersToken import UsersToken
from restapi.models import ApplicationUsers, Application
from restapi.serializers.user_serializer import AppUserSerializer


class AppUserCreate(generics.CreateAPIView):

    """
    Create a user

    Authentication Required:
        NO

    Request:
        POST /register
        {
            "Name": "John Doe",
            "email": "user@test.com",
            "roles": "USER",
            "username": "user",
            "password": "password",
            "appID": 1
        }

    Response:
        201: User created successfully
        400: Bad request

    """
    queryset = ApplicationUsers.objects.all()
    serializer_class = AppUserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = AppUserSerializer(data=data)
        if serializer.is_valid():
            appID = self.request.data.get('appID', None)
            if appID is None:
                return Response({'error': 'appID is required'}, status=status.HTTP_400_BAD_REQUEST)
            application = Application.objects.get(id=appID)
            if application.is_active is False:
                return Response({'error': 'Application is not active'}, status=status.HTTP_400_BAD_REQUEST)
            subscription = Application.getActiveSubscription(application)
            if subscription:
                userCounts = ApplicationUsers.objects.filter(application=appID).count()
                if userCounts >= subscription.package.userAllowed:
                    return Response({'error': 'User limit exceeded'}, status=status.HTTP_400_BAD_REQUEST)


            serializer.save()
            return Response({'success': 'User added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)



class AppUserUpdate(generics.UpdateAPIView):
    """
    Update a user

    Authentication Required:
        Yes (User Token Required)

    Request:
        PUT /update
        {
            "id": 1,
            "Name": "John Doe",
            "email": "",
            "roles": "USER",
        }



    Response:
        200: User updated successfully
        400: Bad request


    """
    authentication_classes = [UsersToken]
    permission_classes = [IsAuthenticated]
    queryset = ApplicationUsers.objects.all()
    serializer_class = AppUserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print("INSTANCE", instance)
        data = request.data
        print("-------DATA ----", data)
        password = self.request.data.get('password', None)
        if password is not None:
            instance.set_password(request.data["password"])

        email = self.request.data.get('email', None)
        if email is not None:
            request.data.pop("email")

        roles = self.request.data.get('roles', None)
        if roles is not None:
            request.data.pop("roles")
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        instance.Name = self.request.data.get('Name', instance.Name)

        instance.save()
        return Response({'success': 'User updated successfully'}, status=status.HTTP_200_OK)