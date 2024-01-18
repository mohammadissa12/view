from django.contrib import admin
from uuid import UUID
# Register your models here.
from .models import *

admin.site.register(AppDetails)


class CustomAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return request.user.is_editor

    def has_delete_permission(self, request, obj=None):
        return request.user.is_deleter


class ExpiredMerchantFilter(admin.SimpleListFilter):
    title = 'merchant expiry'
    parameter_name = 'expiry'

    def lookups(self, request, model_admin):
        return (
            ('expired', 'Expired'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'expired':
            return queryset.filter(merchant_expiry_date__lt=timezone.now().date())


@admin.register(EmailAccount)
class EmailAccountAdmin(admin.ModelAdmin):
    list_display = (
    'phone_number', 'first_name', 'last_name', 'is_merchant', 'merchant_expiry_date', 'get_merchant_expiry_time', 'id')
    list_filter = ('is_merchant', ExpiredMerchantFilter)
    search_fields = ('phone_number', 'first_name',)

    def get_merchant_expiry_time(self, obj):
        if obj.is_merchant and obj.merchant_expiry_date:
            remaining_days = obj.merchant_expiry_date - datetime.date.today()
            return f"{remaining_days.days} days"
        return None

    get_merchant_expiry_time.short_description = 'Time to Expire'

    def has_change_permission(self, request, obj=None):
        if (request.user.id == UUID('b35e6c99-37d6-4633-978f-e49db15f8381') or
                request.user.id == UUID('fe5e31fa-1693-4046-bd4d-b98942a8338a')):
            return True
        return False

    def has_delete_permission(self, request, obj=None):
        if (request.user.id == UUID('b35e6c99-37d6-4633-978f-e49db15f8381') or
                request.user.id == UUID('fe5e31fa-1693-4046-bd4d-b98942a8338a')):
            return True
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-created')
