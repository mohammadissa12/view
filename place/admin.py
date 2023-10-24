from django.contrib import admin
from django.utils.safestring import mark_safe
from account.admin import CustomAdmin

from location.models import Country

from .models import (
    Images,
    Reviews,
    SocialMedia, Advertisement, RecommendedPlaces, LatestPlaces, PlaceMixin, FavoritePlaces, Offers, Company,
    TripDetails, TripImages, PlaceType, PlaceSubType,
)


class PlaceMixinInline(admin.TabularInline):
    extra = 1
    inlines = []


class SocialMediaInline(PlaceMixinInline):
    model = SocialMedia


class ImageInline(PlaceMixinInline):
    model = Images


class ReviewsInline(PlaceMixinInline):
    model = Reviews





class BaseModelAdmin(admin.ModelAdmin):
    inlines = [ImageInline, SocialMediaInline, ReviewsInline]
    list_display = ['name', 'city', 'country_name', 'average_rating', 'count_reviews','place_type','display_images']
    search_fields = ['name', 'city__city_name', 'city__country__country_name','user__first_name']
    list_filter = ['city', 'city__country__country_name', 'place_type__name','type','user__is_merchant',]

    def display_images(self, obj):
        images = obj.place_images.all()

        html = ""
        for image in images:
            html += f'<img src="{image.image_url}" width="80" height="80" />'

        return mark_safe(html)

    display_images.short_description = 'Images'
    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.get_average_rating()

    def count_reviews(self, obj):
        return obj.get_review_count()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'
    count_reviews.short_description = 'عدد التقييمات'


class CountryFilter(admin.SimpleListFilter):
    title = 'Country'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        countries = Country.objects.all()
        return [(country.id, country.country_name) for country in countries]

    def queryset(self, request, queryset):
        return queryset.filter(country__id=self.value()) if self.value() else queryset

    def has_change_permission(self, request, obj=None):
        return request.user.is_editor

    def has_delete_permission(self, request, obj=None):
        return request.user.is_deleter



@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_filter = ['reported','entity_type',]
    list_display = ['user','place','company']

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [SocialMediaInline, ReviewsInline]
    list_display = ['company_name', 'country', 'city', 'company_description']
    search_fields = ['name', 'country__country_name', 'city__city_name']
    list_filter = ['country', 'city']


class ImageTripInline(admin.TabularInline):
    model = TripImages
    extra = 1
    inlines = []


class TripDetailsModelAdmin(admin.ModelAdmin):
    inlines = [ImageTripInline]
    list_display = [ 'trip_name', 'trip_details',]
    search_fields = ['trip__trip_name', 'trip__company__company_name']
    list_filter = []


admin.site.register(TripDetails, TripDetailsModelAdmin)


@admin.register(PlaceMixin)
class PlaceMixinAdmin(BaseModelAdmin):
    def has_change_permission(self, request, obj=None):
        return request.user.is_editor

    def has_delete_permission(self, request, obj=None):
        return request.user.is_deleter


admin.site.register(Advertisement, CustomAdmin)
admin.site.register(LatestPlaces, CustomAdmin)
admin.site.register(RecommendedPlaces, CustomAdmin)
admin.site.register(FavoritePlaces, CustomAdmin)
admin.site.register(Offers, CustomAdmin)

