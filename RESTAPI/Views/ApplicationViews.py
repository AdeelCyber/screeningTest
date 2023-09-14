from rest_framework import generics, status

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from RESTAPI.CustomTokens.SuperAdminToken import SuperAdminAuthentication
from RESTAPI.Serializers.ApplicationSerializer import ApplicationSerializer
from RESTAPI.models import Application, Subscriptions


class ApplicationCreate(generics.CreateAPIView):
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
            try:
                newSub = Subscriptions.objects.create(application=application)
                newSub.save()
                return Response({'success': 'Application added successfully'}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': 'Subscription not created'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ApplicationList(generics.ListAPIView):
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
    authentication_classes = [SuperAdminAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, pk=self.kwargs['pk'])
        return obj


class ApplicationUpdate(generics.UpdateAPIView):
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
