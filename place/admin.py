from django.contrib import admin
from nested_inline.admin import NestedModelAdmin

from .models import (
    StayPlace,
    Restaurant,
    Cafeteria,
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
    Reviews,
    SocialMedia,
    # Advertisement,
)


class PlaceMixinInline(admin.TabularInline):
    extra = 1
    inlines = []


class ContactInline(PlaceMixinInline):
    model = SocialMedia


class ImageInline(PlaceMixinInline):
    model = Images


class ReviewsInline(PlaceMixinInline):
    model = Reviews


class StayPlaceInline(PlaceMixinInline):
    model = StayPlace


class RestaurantInline(PlaceMixinInline):
    model = Restaurant


class CafeteriaInline(PlaceMixinInline):
    model = Cafeteria


class MallInline(PlaceMixinInline):
    model = Mall


class HealthCentreInline(PlaceMixinInline):
    model = HealthCentre


class SalonsInline(PlaceMixinInline):
    model = Salons


class TouristPlaceInline(PlaceMixinInline):
    model = TouristPlace


class GymInline(PlaceMixinInline):
    model = Gym


class HolyPlaceInline(PlaceMixinInline):
    model = HolyPlace


class FinancialInline(PlaceMixinInline):
    model = Financial


class GasStationInline(PlaceMixinInline):
    model = GasStation


class EntertainmentInline(PlaceMixinInline):
    model = Entertainment


class BaseModelAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ContactInline, ReviewsInline]
    list_display = ['name', 'city', 'country_name', 'average_rating', 'count_reviews']
    search_fields = ['name', 'city__city_name', 'city__country__country_name']
    list_filter = ['city', 'city__country__country_name']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    def count_reviews(self, obj):
        return obj.count_reviews()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'
    count_reviews.short_description = 'عدد التقييمات'


@admin.register(StayPlace)
class StayPlaceAdmin(BaseModelAdmin):
    pass


@admin.register(Restaurant)
class RestaurantAdmin(BaseModelAdmin):
    pass


@admin.register(Cafeteria)
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


# @admin.register(Advertisement)
# class AdvertisementAdmin(NestedModelAdmin):
#     list_display = ['title', 'place', 'start_date', 'end_date', 'is_active']