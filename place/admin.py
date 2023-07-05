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
    Reviews,
    Gym,
    HolyPlace,
    Financial,
    GasStation,
    Entertainment, PlaceMixin,
    Reviews
)


class PlaceMixinInline(admin.TabularInline):
    extra = 1
    inlines = []


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


@admin.register(StayPlace)
class StayPlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewsInline]

    list_display = ['name', 'city', 'country_name', 'type', 'average_rating']
    search_fields = ['name', 'city__city_name', 'city__country__country_name', 'type']
    list_filter = ['city', 'city__country__country_name', 'type', ]

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewsInline]

    list_display = ['name', 'city', 'country_name', 'average_rating']
    search_fields = ['name', 'city__city_name', 'city__country__country_name']
    list_filter = ['city', 'city__country__country_name']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'


@admin.register(Cafeteria)
class CafeteriaAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewsInline]

    list_display = ['name', 'city', 'country_name', 'average_rating']
    search_fields = ['name', 'city__city_name', 'city__country__country_name']
    list_filter = ['city', 'city__country__country_name']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'


@admin.register(Mall)
class MallAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewsInline]
    list_display = ['name', 'city', 'country_name', 'average_rating']
    search_fields = ['name', 'city__city_name', 'city__country__country_name']
    list_filter = ['city', 'city__country__country_name']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'


@admin.register(HealthCentre)
class HealthCentreAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewsInline]
    list_display = ['name', 'city', 'country_name', 'type', 'average_rating']
    search_fields = ['name', 'city__city_name', 'city__country__country_name', 'type']
    list_filter = ['city', 'city__country__country_name', 'type']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'


@admin.register(Salons)
class SalonsAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewsInline]
    list_display = ['name', 'city', 'country_name', 'type', 'average_rating']
    search_fields = ['name', 'city__city_name', 'city__country__country_name', 'type']
    list_filter = ['city', 'city__country__country_name', 'type']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'


@admin.register(TouristPlace)
class TouristPlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewsInline]
    list_display = ['name', 'city', 'country_name', 'type', 'average_rating']
    search_fields = ['name', 'city__city_name', 'city__country__country_name', 'type']
    list_filter = ['city', 'city__country__country_name', 'type']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'


@admin.register(Gym)
class GymAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewsInline]
    list_display = ['name', 'city', 'country_name', 'average_rating']
    search_fields = ['name', 'city__city_name', 'city__country__country_name']
    list_filter = ['city', 'city__country__country_name']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'


@admin.register(HolyPlace)
class HolyPlaceAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewsInline]
    list_display = ['name', 'city', 'country_name', 'type', 'average_rating']
    search_fields = ['name', 'city__city_name', 'city__country__country_name', 'type']
    list_filter = ['city', 'city__country__country_name', 'type']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'


@admin.register(Financial)
class FinancialAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewsInline]
    list_display = ['name', 'city', 'country_name', 'type', 'average_rating']
    search_fields = ['name', 'city__city_name', 'city__country__country_name', 'type']
    list_filter = ['city', 'city__country__country_name', 'type']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'


@admin.register(GasStation)
class GasStationAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewsInline]
    list_display = ['name', 'city', 'country_name', 'average_rating']
    search_fields = ['name', 'city__city_name', 'city__country__country_name']
    list_filter = ['city', 'city__country__country_name']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'


@admin.register(Entertainment)
class EntertainmentAdmin(admin.ModelAdmin):
    inlines = [ImageInline, ReviewsInline]
    list_display = ['name', 'city', 'country_name', 'average_rating']
    search_fields = ['name', 'city__city_name', 'city__country__country_name']
    list_filter = ['city', 'city__country__country_name']

    def country_name(self, obj):
        return obj.city.country.country_name

    def average_rating(self, obj):
        return obj.average_rating()

    country_name.short_description = 'الدولة'
    average_rating.short_description = 'متوسط التقييم'


admin.site.register(Reviews)