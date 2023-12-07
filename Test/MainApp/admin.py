from django.contrib import admin
from .models import *

admin.site.registration(CustomUser)
admin.site.registration(UsersFiles)
admin.site.registration(Roles)
admin.site.registration(UserStatus)