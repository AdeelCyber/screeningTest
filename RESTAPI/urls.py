from django.urls import path

from .Views.ApplicationViews import ApplicationCreate, ApplicationList, ApplicationDetail, ApplicationUpdate, \
    ApplicationDelete
from .Views.AuthViews import LoginView
from .Views.SubscriptionViews import SubscriptionDelete, SubscriptionUpdate, SubscriptionList
from .Views.UserViews import AppUserCreate

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
