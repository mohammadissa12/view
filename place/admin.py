from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from nested_inline.admin import NestedModelAdmin

from location.models import Country
from .models import (
    StayPlace,
    Restaurant,
    Cafe,
    Mall,
    HealthCentre,
    Salons,
    TouristPlace,
    Images,
    Gym,
    HolyPlace,
    Financial,
    GasStation,
    Entertainment,
    Images,
    Reviews,
    SocialMedia, Advertisement, RecommendedPlaces, LatestPlaces, PlaceMixin, FavoritePlaces
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
    list_display = ['name', 'city', 'country_name', 'average_rating', 'count_reviews']
    search_fields = ['name', 'city__city_name', 'city__country__country_name']
    list_filter = ['city', 'city__country__country_name']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.get_average_rating()

    def count_reviews(self, obj):
        return obj.get_review_count()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'
    count_reviews.short_description = 'عدد التقييمات'


@admin.register(StayPlace)
class StayPlaceAdmin(BaseModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(BaseModelAdmin):
    pass


@admin.register(Cafe)
class CafeteriaAdmin(BaseModelAdmin):
    pass


@admin.register(Mall)
class MallAdmin(BaseModelAdmin):
    pass


@admin.register(HealthCentre)
class HealthCentreAdmin(BaseModelAdmin):
    pass


@admin.register(Salons)
class SalonsAdmin(BaseModelAdmin):
    pass


@admin.register(TouristPlace)
class TouristPlaceAdmin(BaseModelAdmin):
    pass


@admin.register(Gym)
class GymAdmin(BaseModelAdmin):
    pass


@admin.register(HolyPlace)
class HolyPlaceAdmin(BaseModelAdmin):
    pass


@admin.register(Financial)
class FinancialAdmin(BaseModelAdmin):
    pass


@admin.register(GasStation)
class GasStationAdmin(BaseModelAdmin):
    pass


@admin.register(Entertainment)
class EntertainmentAdmin(BaseModelAdmin):
    pass


class CountryFilter(admin.SimpleListFilter):
    title = 'Country'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        countries = Country.objects.all()
        return [(country.id, country.country_name) for country in countries]

    def queryset(self, request, queryset):
        return queryset.filter(country__id=self.value()) if self.value() else queryset


class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['country', 'title', 'content_type', 'start_date', 'end_date', 'is_active']
    list_filter = [CountryFilter, 'is_active']
    # Specify the fields to be displayed in the change form
    fields = ['country', 'content_type', 'place','title', 'image', 'short_description', 'url', 'start_date', 'end_date',
              'is_active']

    # Override the formfield_for_foreignkey method
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'content_type':
            kwargs['queryset'] = ContentType.objects.filter(model__in=['restaurant', 'cafeteria', 'mall',
                                                                       'healthcentre', 'salons', 'touristplace',
                                                                       'gym', 'holyplace', 'financial', 'gasstation',
                                                                       'entertainment', 'stayplace'])
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Advertisement, AdvertisementAdmin)
admin.site.register(LatestPlaces)
admin.site.register(RecommendedPlaces)
admin.site.register(FavoritePlaces)
