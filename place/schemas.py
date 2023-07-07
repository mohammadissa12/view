from ninja import Schema
from pydantic import UUID4
from typing import List, Optional

from account.schemas import Profile
from location.schemas import CityOut


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


# class AdvertisementOut(Schema):
#     id: UUID4
#     title: Optional[str]
#     description: Optional[str]
#     image: Optional[str]
#     link: Optional[str]
#     place: Optional[PlaceMixinOut]
#     location: Optional[str]
#     start_date: Optional[str]
#     end_date: Optional[str]
#     is_active: bool
