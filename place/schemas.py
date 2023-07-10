from datetime import date

from ninja import Schema
from pydantic import UUID4, Field, BaseModel
from typing import List, Optional

from account.schemas import Profile
from location.schemas import CityOut, CountryOut


class ProductImageOut(Schema):
    id: UUID4
    image: str


class PlaceMixinOut(Schema):
    id: UUID4
    name: str
    location: str
    city: CityOut
    description: Optional[str]
    place_details: Optional[str]
    short_location: Optional[str]
    type: Optional[str]
    place_images: List[ProductImageOut]

    class Config:
        orm_mode = True


class PlaceMixinSchema(Schema):
    total_count: int = None
    per_page: int = None
    from_record: int = None
    to_record: int = None
    previous_page: int = None
    next_page: int = None
    current_page: int = None
    page_count: int = None
    data: List[PlaceMixinOut]


class ContentTypeOut(Schema):
    app_label: str
    model: str

    class Config:
        orm_mode = True


class AdvertisementSchema(Schema):
    id: UUID4
    country: CountryOut
    content_type: ContentTypeOut = None
    image: str
    title: str
    short_description: str
    url: str = None
    place: PlaceMixinOut = None
    start_date: date
    end_date: date
    is_active: bool


class RecommendedPlacesOut(Schema):
    id: UUID4
    country: CountryOut
    place: PlaceMixinOut

