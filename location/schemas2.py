from typing import List

from ninja import Schema, ModelSchema
from ninja.orm import create_schema
from pydantic import UUID4

from location.models import Country
from location.schemas import CountryOut, CityOut
from place.schemas import AdvertisementSchema, RecommendedPlacesOut, LatestPlacesOut


class CountryInfoSchema(Schema):
    get_cities: List[CityOut]


class CountryInfoSchema2(ModelSchema):

    class Config:
        # model = Adver
        model_exclude=['id']

class CountryRecommendedPlacesOut(Schema):
    get_recommended_places: List[RecommendedPlacesOut]

    class Config:
        orm_mode = True
