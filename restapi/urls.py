from django.urls import path

from restapi.views.application_views import *
from restapi.views.auth_views import LoginView
from restapi.views.subscription_views import *
from restapi.views.user_views import AppUserCreate

urlpatterns = [
    path("login", LoginView),


    path("createApplication", ApplicationCreate.as_view()),
    path("listApplications", ApplicationList.as_view()),
    path("applicationDetail/<int:pk>", ApplicationDetail.as_view()),
    path("updateApplication/<int:pk>", ApplicationUpdate.as_view()),
    path("deleteApp/<int:pk>", ApplicationDelete.as_view()),

    path("deleteSubscription/<int:pk>", SubscriptionDelete.as_view()),
    path("SubscriptionUpdate/<int:pk>", SubscriptionUpdate.as_view()),
    path("SubscriptionList", SubscriptionList.as_view()),
    path("register", AppUserCreate.as_view()),
]
