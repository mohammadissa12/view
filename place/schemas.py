from datetime import date

from ninja import Schema
from pydantic import UUID4, Field, BaseModel
from typing import List, Optional

from account.schemas import Profile, AccountOut
from location.schemas import CityOut, CountryOut


class ProductImageOut(Schema):
    id: UUID4
    image: str


class SocialMediaOut(BaseModel):
    id: UUID4
    facebook: Optional[str] = None
    instagram: Optional[str] = None
    telegram: Optional[str] = None
    twitter: Optional[str] = None
    is_available: Optional[bool] = None


class PlaceOut(Schema):
    id: UUID4
    name: str
    location: str
    city: CityOut
    place_type: str = Field(..., description='Place type: hotel, restaurant, etc.')
    description: Optional[str]
    place_details: Optional[str]
    short_location: Optional[str]
    type: Optional[str]
    place_images: List[ProductImageOut]


class PlaceSchema(Schema):
    total_count: int = None
    per_page: int = None
    from_record: int = None
    to_record: int = None
    previous_page: int = None
    next_page: int = None
    current_page: int = None
    page_count: int = None
    data: List[PlaceOut]


class AdvertisementSchema(Schema):
    id: UUID4
    country: CountryOut
    place_type: str = Field(..., description='Place type: hotel, restaurant, etc.')
    image: str
    title: str
    short_description: str
    url: str = None
    place: PlaceOut = None
    start_date: date
    end_date: date
    is_active: bool


class RecommendedPlacesOut(Schema):
    id: UUID4
    country: CountryOut
    place: PlaceOut


class LatestPlacesOut(Schema):
    id: UUID4
    country: CountryOut
    place: PlaceOut


class FavoritePlaceOut(Schema):
    id: UUID4
    place: PlaceOut


class FavoritePlaceIn(Schema):
    place_id: UUID4
