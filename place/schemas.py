from datetime import date

from ninja import Schema
from pydantic import UUID4, Field, BaseModel
from typing import List, Optional
from pydantic import HttpUrl

from account.schemas import Profile, AccountOut
from location.schemas import CityOut, CountryOut
from place.models import PlaceMixin


class SocialMediaSchema(Schema):
    id: UUID4
    facebook: str = None
    whatsapp: str = None
    instagram: str = None
    telegram: str = None


class PlaceImageOut(Schema):
    id: UUID4
    image: str


class PlaceMixinOut(Schema):
    id: UUID4
    name: str
    # location: str
    city: CityOut
    longitude: float
    latitude: float
    description: str
    short_location: str
    place_images: List[PlaceImageOut]
    type: Optional[str]
    # social_media: Optional[SocialMediaSchema] = None
    average_rating: Optional[float]


    review_count: Optional[int]


    class Config:
        orm_mode = True

    # @staticmethod
    # def from_orm(place: PlaceMixin):
    #     return PlaceMixinOut(
    #         social_media=[SocialMediaSchema.from_orm(place.get_social_media)] if place.social_media else None,)



# class PlaceMixinSchema(Schema):
#     total_count: int = None
#     per_page: int = None
#     from_record: int = None
#     to_record: int = None
#     previous_page: int = None
#     next_page: int = None
#     current_page: int = None
#     page_count: int = None
#     data: List[PlaceMixinOut]


class ReviewsSchema(Schema):
    id: UUID4
    user: AccountOut
    place_id: UUID4
    comment: Optional[str]
    rating: int


class ReviewsIn(Schema):
    comment: Optional[str]
    rating: int


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


class LatestPlacesOut(Schema):
    id: UUID4
    country: CountryOut
    place: PlaceMixinOut


class FavoritePlaceOut(Schema):
    id: UUID4
    place: PlaceMixinOut


class FavoritePlaceIn(Schema):
    place_id: UUID4
