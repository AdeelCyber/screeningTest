from rest_framework import generics, status

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from restapi.CustomTokens.SuperAdminToken import SuperAdminAuthentication
from restapi.serializers.ApplicationSerializer import ApplicationSerializer
from restapi.models import Application, Subscriptions


class ApplicationCreate(generics.CreateAPIView):
    # Generate Docstring for OPTIONS method
    """
    Create an application

    Authentication Required:
        YES (Super Admin)

    Request:
        POST /createApplication
        {
            "name": "Application Name",
            "description": "Application Description",
            "logo": File
        }

    Response:
        201: Application created successfully
        400: Bad request

    """

    authentication_classes = [SuperAdminAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = ApplicationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            application = Application.objects.get(id=serializer.data['id'])
            application.is_active = True
            application.save()
            try:
                newSub = Subscriptions.objects.create(application=application)
                newSub.save()
                return Response({'success': 'Application added successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': 'Subscription not created'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ApplicationList(generics.ListAPIView):
    # Generate Docstring for OPTIONS method
    """
    List all applications

    Authentication Required:
        YES (Super Admin)

    Request:
        GET /listApplications
        {
            "name": "Application Name", (optional)
            "page": 1, (optional)
            page_size: 10 (optional)
        }

    Response:
        200: List of applications
        404: Not found

    """

    authentication_classes = [SuperAdminAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_queryset(self):
        queryset = Application.objects.all().order_by('-id')
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(Q(name__icontains=name))
        return queryset


class ApplicationDelete(generics.DestroyAPIView):
    # Generate Docstring for OPTIONS method

    """
    Delete an application

    Authentication Required:
        YES (Super Admin)

    Request:
        DELETE /deleteApp/<id>

    Response:
        200: Application deleted successfully
        404: Not found
    """
    authentication_classes = [SuperAdminAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_active = False
            instance.save()
            return Response({'success': 'Application deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)


class ApplicationDetail(generics.RetrieveAPIView):

    """
    Get an application

    Authentication Required:
        YES (Super Admin)

    Request:
        GET /applicationDetail/<id>

    Response:
        200: Application details
        404: Not found
    """
    authentication_classes = [SuperAdminAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj


class ApplicationUpdate(generics.UpdateAPIView):

    """
    Update an application

    Authentication Required:
        YES (Super Admin)

    Request:
        PUT /updateApplication/<id>
        {
            "name": "Application Name",
            "description": "Application Description",
            "logo": File
        }
        (Partial update is allowed)

    Response:
        200: Application updated successfully
        404: Not found
    """
    authentication_classes = [SuperAdminAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            data = request.data
            serializer = ApplicationSerializer(instance, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success': 'Application updated successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'Application not found'}, status=status.HTTP_404_NOT_FOUND)
