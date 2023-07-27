from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(EmailAccount)

admin.site.register(ProfileUser)
