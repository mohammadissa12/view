from django.contrib import admin
from django.contrib.admin import RelatedOnlyFieldListFilter

# Register your models here.
from location.models import Country, City
from place.admin import PlaceMixinInline
from place.models import StayPlace, Restaurant, Cafe, Mall, HealthCenter, Salons, TouristPlace, Sport, HolyPlace, \
    Financial, GasStation, Entertainment


class StayPlaceInline(PlaceMixinInline):
    model = StayPlace


class RestaurantInline(PlaceMixinInline):
    model = Restaurant


class CafeteriaInline(PlaceMixinInline):
    model = Cafe


class MallInline(PlaceMixinInline):
    model = Mall


class HealthCentreInline(PlaceMixinInline):
    model = HealthCenter


class SalonsInline(PlaceMixinInline):
    model = Salons


class TouristPlaceInline(PlaceMixinInline):
    model = TouristPlace


class GymInline(PlaceMixinInline):
    model = Sport


class HolyPlaceInline(PlaceMixinInline):
    model = HolyPlace


class FinancialInline(PlaceMixinInline):
    model = Financial


class GasStationInline(PlaceMixinInline):
    model = GasStation


class EntertainmentInline(PlaceMixinInline):
    model = Entertainment


class CityInline(admin.TabularInline):
    model = City
    extra = 1


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    inlines = [CityInline]

    list_display = ['country_name']
    search_fields = ['country_name']
    list_filter = ['country_name']


class CountryFilter(admin.SimpleListFilter):
    title = 'Country'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        countries = Country.objects.all()
        return [(country.id, country.country_name) for country in countries]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(country__id=self.value())
        else:
            return queryset


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    inlines = [StayPlaceInline, RestaurantInline, CafeteriaInline, MallInline, HealthCentreInline, SalonsInline,
               TouristPlaceInline, GymInline, HolyPlaceInline, FinancialInline, GasStationInline, EntertainmentInline]

    list_display = ['city_name', 'country']
    search_fields = ['city_name', 'country__country_name']
    list_filter = [CountryFilter]

    def country(self, obj):
        return obj.country.country_name

    country.admin_order_field = 'country'

    def get_inline_instances(self, request, obj=None):
        if obj is None:
            # Return empty list when creating a new city
            return []
        return super().get_inline_instances(request, obj)