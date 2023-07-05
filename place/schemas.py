from ninja import Schema
from pydantic import UUID4
from typing import List

from account.schemas import Profile
from location.schemas import CityOut


class PlaceMixinOut(Schema):
    id: UUID4
    name: str
    location: str
    city: CityOut
    type: str = None

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


class ReviewOut(Schema):
    id: UUID4
    user: Profile
    place: PlaceMixinOut
    rating: int
    review: str
    created_at: str

    class Config:
        orm_mode = True


class ReviewSchema(Schema):
    total_count: int = None
    per_page: int = None
    from_record: int = None
    to_record: int = None
    previous_page: int = None
    next_page: int = None
    current_page: int = None
    page_count: int = None
    data: List[ReviewOut]

# class RestaurantOut(PlaceMixinOut):
#     pass
#
#
# class StayPlaceOut(PlaceMixinOut):
#     type: str
#
#
# class CafeteriaOut(PlaceMixinOut):
#     pass
#
#
# class TouristPlaceOut(Schema):
#     type: str
#
#
# class MallOut(PlaceMixinOut):
#     pass
#
#
# class HealthCentreOut(PlaceMixinOut):
#     type: str
#
#
# class HolyPlaceOut(PlaceMixinOut):
#     type: str
#
#
# class FinancialOut(PlaceMixinOut):
#     type: str
#
#
# class GasStationOut(PlaceMixinOut):
#     pass
#
#
# class EntertainmentOut(PlaceMixinOut):
#     pass
#
#
# class GymOut(PlaceMixinOut):
#     pass
#
#
# class SalonsOut(PlaceMixinOut):
#     type: str
#
#
# class RestaurantSchema(PlaceMixinSchema):
#     data: List[RestaurantOut]
#
#
# class StayPlaceSchema(PlaceMixinSchema):
#     data: List[StayPlaceOut]
#
#
# class CafeteriaSchema(PlaceMixinSchema):
#     data: List[CafeteriaOut]
#
#
# class TouristPlaceSchema(PlaceMixinSchema):
#     data: List[TouristPlaceOut]
