from django.contrib import admin

# Register your models here.
from .models import Request

from .models import Reviews, UserInformation, PointOfInterest, Request

admin.site.register(Reviews)
admin.site.register(UserInformation)
admin.site.register(PointOfInterest)
admin.site.register(Request)
