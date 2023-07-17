from typing import List

from ninja import Schema, ModelSchema
from ninja.orm import create_schema
from pydantic import UUID4

from location.models import Country
from location.schemas import CountryOut, CityOut
from place.models import Advertisement
from place.schemas import AdvertisementSchema, RecommendedPlacesOut, LatestPlacesOut


class CountrySchema2(Schema):
    country_name: str
    cities: List[CityOut]
    advertisements: List[AdvertisementSchema]
    recommended_places: List[RecommendedPlacesOut]
    latest_places: List[LatestPlacesOut]

    @staticmethod
    def from_orm(country: Country):
        return CountrySchema2(
            country_name=country.country_name,
            cities=[CityOut.from_orm(city) for city in country.get_cities],
            advertisements=[AdvertisementSchema.from_orm(ad) for ad in country.get_advertisements],
            recommended_places=[RecommendedPlacesOut.from_orm(place) for place in country.get_recommended_places],
            latest_places=[LatestPlacesOut.from_orm(place) for place in country.get_latest_places]
        )
