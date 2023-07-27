from django.contrib import admin


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
    Sport,
    HolyPlace,
    Financial,
    GasStation,
    Entertainment,
    Images,
    Reviews,
    SocialMedia, Advertisement, RecommendedPlaces, LatestPlaces, PlaceMixin, FavoritePlaces, Offers, Company, Trip,
    TripDetails
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


@admin.register(Sport)
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




admin.site.register(Advertisement)
admin.site.register(LatestPlaces)
admin.site.register(RecommendedPlaces)
admin.site.register(FavoritePlaces)
admin.site.register(Offers)
admin.site.register(Company)
admin.site.register(Trip)
admin.site.register(TripDetails)