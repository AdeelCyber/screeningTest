from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Users)
admin.site.register(Packages)
admin.site.register(Application)
admin.site.register(Subscriptions)
admin.site.register(ApplicationUsers)

