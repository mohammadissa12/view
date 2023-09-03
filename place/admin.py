from django.contrib import admin
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
    list_display = ['name', 'city', 'country_name', 'average_rating', 'count_reviews','place_type']
    search_fields = ['name', 'city__city_name', 'city__country__country_name']
    list_filter = ['city', 'city__country__country_name', 'place_type__name','type','type__place_type',]

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


admin.site.register(Advertisement)
admin.site.register(LatestPlaces)
admin.site.register(RecommendedPlaces)
admin.site.register(FavoritePlaces)
admin.site.register(Offers)





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

'''place_type'''
admin.site.register(PlaceType)
admin.site.register(PlaceSubType)


@admin.register(PlaceMixin)
class PlaceMixinAdmin(BaseModelAdmin):
    pass