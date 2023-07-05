from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(EmailAccount)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'user')


admin.site.register(ProfileUser, ImageAdmin)

