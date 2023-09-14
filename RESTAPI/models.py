from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager
from .roles import *


class Users(AbstractUser):
    username = models.CharField(max_length=100, null=False, blank=False, unique=True,
                                error_messages={'unique': 'A user with that username already exists.'})
    first_name = None
    last_name = None
    email = models.EmailField(max_length=100, null=False, blank=False, unique=True)
    USERNAME_FIELD = "email"
    roles = models.CharField(max_length=100, choices=ROLES, default=USER)
    Name = models.CharField(max_length=100, null=False, blank=False)
    REQUIRED_FIELDS = ['Name', 'username', 'roles']
    objects = CustomUserManager()

    def isUserSuperAdmin(self):
        return self.roles == SUPER_ADMIN

    def isUserUser(self):
        return self.roles == USER

    def __str__(self):
        return self.Name + " " + self.email


class Packages(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    price = models.FloatField(null=False, blank=False)
    userAllowed = models.IntegerField(null=False, blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    updated_at = models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return self.name + " " + str(self.price)


class Application(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=100, null=False, blank=False)
    logo = models.ImageField(upload_to="applicationLogo", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name + " " + str(self.is_active)

    @staticmethod
    def getActiveSubscription(applicationID):
        try:
            application = Application.objects.get(id=applicationID)
            subscription = Subscriptions.objects.filter(application=application, is_active=True)
            if subscription.exists():
                return subscription[0]
            else:
                return False
        except Exception as e:
            return False


class Subscriptions(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    package = models.ForeignKey(Packages,default=1, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.application.name + " " + self.package.name + " " + str(self.is_active)


class ApplicationUsers(Users):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.application.name +" " + self.Name + " " + self.email
