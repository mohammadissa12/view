from django.contrib import admin
from django.contrib.admin import RelatedOnlyFieldListFilter

# Register your models here.
from location.models import Country, City
from place.admin import StayPlaceInline, RestaurantInline, CafeteriaInline, MallInline, HealthCentreInline, SalonsInline, \
    HolyPlaceInline, EntertainmentInline, TouristPlaceInline, FinancialInline, GasStationInline, GymInline


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


