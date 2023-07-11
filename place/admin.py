from django.contrib import admin
from django.contrib.contenttypes.models import ContentType
from django.utils.html import format_html
from nested_inline.admin import NestedModelAdmin

from location.models import Country
from .models import (
    Images,
    Reviews,
    SocialMedia, Advertisement, RecommendedPlaces, LatestPlaces, PlaceMixin, FavoritePlaces
)


class PlaceMixinInline(admin.TabularInline):
    model = PlaceMixin
    extra = 1
    inlines = []


class SocialMediaInline(PlaceMixinInline):
    model = SocialMedia


class ImageInline(admin.TabularInline):
    model = Images

    def image_preview(self, obj):
        return format_html('<img src="{}" width="120" height="" />', obj.image.url)

    readonly_fields = ('image_preview',)
    fields = ('image', 'image_preview')
    extra = 0


class ReviewsInline(PlaceMixinInline):
    model = Reviews


class PlaceAdmin(admin.ModelAdmin):
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


admin.site.register(PlaceMixin, PlaceAdmin)

admin.site.register(FavoritePlaces)
admin.site.register(Advertisement)
admin.site.register(LatestPlaces)
admin.site.register(RecommendedPlaces)

#
