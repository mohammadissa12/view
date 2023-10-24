from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(AppDetails)


class CustomAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return request.user.is_editor

    def has_delete_permission(self, request, obj=None):
        return request.user.is_deleter


class EmailAccountAdmin(admin.ModelAdmin):
    list_display = (
    'phone_number', 'first_name', 'last_name', 'is_merchant', 'merchant_expiry_date', 'get_merchant_expiry_time', 'id')
    list_filter = ('is_merchant',)
    search_fields = ('phone_number', 'first_name',)

    def get_merchant_expiry_time(self, obj):
        if obj.is_merchant and obj.merchant_expiry_date:
            remaining_days = obj.merchant_expiry_date - datetime.date.today()
            return f"{remaining_days.days} days"
        return None

    get_merchant_expiry_time.short_description = 'Time to Expire'

    def has_change_permission(self, request, obj=None):
        return request.user.is_editor

    def has_delete_permission(self, request, obj=None):
        return request.user.is_deleter

admin.site.register(EmailAccount, EmailAccountAdmin)
