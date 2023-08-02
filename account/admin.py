from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(AppDetails)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('account', )
    list_filter = ('account__is_merchant',)


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    list_display = ('account', )


@admin.register(EmailAccount)
class EmailAccountAdmin(admin.ModelAdmin):
    list_display = ('phone_number','first_name', 'last_name', 'is_merchant')
    list_filter = ('is_merchant',)