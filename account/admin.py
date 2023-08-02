from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(AppDetails)

@admin.register(EmailAccount)
class EmailAccountAdmin(admin.ModelAdmin):
    list_display = ('phone_number','first_name', 'last_name', 'is_merchant')
    list_filter = ('is_merchant',)