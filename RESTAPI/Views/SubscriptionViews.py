from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from rest_framework import generics, status

from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from RESTAPI.CustomTokens.SuperAdminToken import SuperAdminAuthentication
from RESTAPI.Serializers.ApplicationSerializer import ApplicationSerializer
from RESTAPI.Serializers.SubscriptionSerializer import SubscriptionSerializer
from RESTAPI.models import Subscriptions, Packages


class SubscriptionDelete(generics.DestroyAPIView):
    authentication_classes = [SuperAdminAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionSerializer

    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.is_active = False
            instance.save()
            return Response({'success': 'Subscription deleted successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionUpdate(generics.UpdateAPIView):
    authentication_classes = [SuperAdminAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionSerializer

    def update(self, request, *args, **kwargs):
        data = request.data
        print(data)

        subscription_id = data.get('subscription_id', None)
        action = data.get('action', None)
        if subscription_id is None or action is None:
            return Response({'error': 'subscription_id and action are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            subscription = Subscriptions.objects.get(id=subscription_id)
        except ObjectDoesNotExist:
            return Response({'error': 'subscription not found'}, status=status.HTTP_404_NOT_FOUND)
        print(action)
        if action == 'activate':
            subscription.is_active = True
            subscription.save()
            return Response({'success': 'subscription activated'}, status=status.HTTP_200_OK)
        elif action == 'upgradeTo':
            print("UPGRADE TO")
            package_id = data.get('package_id', None)
            if package_id is None:
                return Response({'error': 'package_id is required'}, status=status.HTTP_400_BAD_REQUEST)
            subscription.is_active = False
            subscription.save()

            try:
                # make is_active false for all subscriptions of this application
                subscriptions = Subscriptions.objects.filter(application=subscription.application)
                for sub in subscriptions:
                    sub.is_active = False
                    sub.save()
                newSub = Subscriptions.objects.create(application=subscription.application)
                package = Packages.objects.get(id=package_id)
                newSub.package = package
                newSub.save()
                return Response({'success': 'subscription upgraded'}, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': 'package not found'}, status=status.HTTP_404_NOT_FOUND)




        return Response({'error': 'invalid action'}, status=status.HTTP_400_BAD_REQUEST)


class SubscriptionList(generics.ListAPIView):
    authentication_classes = [SuperAdminAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        queryset = Subscriptions.objects.all().order_by('-id')
        appID = self.request.query_params.get('applicationID', None)
        if appID is not None:
            queryset = queryset.filter(Q(application__id=appID))
        return queryset
