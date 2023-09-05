from typing import List
from ninja import Schema
from pydantic import UUID4
from django.db.models import Subquery, OuterRef, FloatField, Avg

import account.models
from account.schemas import AppDetails
from location.models import Country, City
from location.schemas import CountryOut, CityOut
from place.models import Advertisement, PlaceMixin, Reviews
from place.schemas import AdvertisementSchema, RecommendedPlacesOut, LatestPlacesOut, PlaceMixinOut, OfferSchema



class CountrySchema2(Schema):
    app_version: str = None
    ios_link: str = None
    android_link: str = None
    country_id: UUID4 = None
    country_name: str
    cities: List[CityOut]
    advertisements: List[AdvertisementSchema]
    recommended_places: List[RecommendedPlacesOut]
    offers: List[OfferSchema]
    companies_with_cities: List[dict] = None

    @staticmethod
    def from_orm(country: Country):
        companies_with_cities = []

        for company in country.get_company:
            company_info = {
                "city_name": company.city.city_name if company.city else None,
                # "associated_city_id": company.city.id.hex if company.city else None
            }
            companies_with_cities.append(company_info)

        return CountrySchema2(
            country_id=country.id,
            country_name=country.country_name,
            cities=[CityOut.from_orm(city) for city in country.get_cities],
            advertisements=[AdvertisementSchema.from_orm(ad) for ad in country.get_advertisements],
            recommended_places=[RecommendedPlacesOut.from_orm(place) for place in country.get_recommended_places],
            offers=[OfferSchema.from_orm(offer) for offer in country.get_offers],
            companies_with_cities=companies_with_cities,
            app_version=AppDetails.from_orm(account.models.AppDetails.objects.first()).app_version,
            ios_link=AppDetails.from_orm(account.models.AppDetails.objects.first()).ios_link,
            android_link=AppDetails.from_orm(account.models.AppDetails.objects.first()).android_link,
        )

class CitySchema2(Schema):
    city_id: UUID4 = None
    city_name: str
    country: CountryOut
    advertisements: List[AdvertisementSchema]
    latest_places: List[LatestPlacesOut]
    highest_rated_places: List[PlaceMixinOut]

    @staticmethod
    def from_orm(city: City):
        highest_rated_places = PlaceMixin.objects.filter(city=city).annotate(
            avg_rating=Avg('reviews__rating')
        ).filter(
            avg_rating__isnull=False
        ).order_by(
            '-avg_rating'
        )[:10]  # You can adjust the number as needed

        return CitySchema2(
            city_id=city.id,
            city_name=city.city_name,
            country=CountryOut.from_orm(city.country),
            advertisements=[AdvertisementSchema.from_orm(ad) for ad in city.get_advertisements],
            latest_places=[LatestPlacesOut.from_orm(place) for place in city.get_latest_places],
            highest_rated_places=[PlaceMixinOut.from_orm(place) for place in highest_rated_places]
        )
