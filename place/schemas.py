from ninja import Schema
from pydantic import UUID4
from typing import List, Optional
from pydantic import HttpUrl

from account.schemas import  AccountOut
from location.schemas import CityOut, CountryOut
from place.models import PlaceMixin, StayPlace, TouristPlace, HealthCentre, HolyPlace, Financial, GasStation, \
    Entertainment, Sport, Salons, Restaurant, Cafe, Mall


class SocialMediaSchema(Schema):
    facebook: str = None
    instagram: str = None
    telegram: str = None
    whatsapp: str = None
    is_available: List[str] = None


class PlaceImageOut(Schema):
    id: UUID4
    image: str
    image_url: HttpUrl


class PlaceMixinOut(Schema):
    id: UUID4
    name: str
    # location: str
    city: CityOut
    longitude: float
    latitude: float
    description: str
    short_location: str
    price: Optional[str]
    place_images: List[PlaceImageOut]
    social_media: Optional[SocialMediaSchema]
    type: Optional[str]
    subtype: Optional[str]
    average_rating: Optional[float]
    review_count: Optional[int]
    available: Optional[str]


    class Config:
        orm_mode = True

    @staticmethod
    def from_orm(place: PlaceMixin):
        is_available = place.get_social_media

        if isinstance(place, Restaurant):

            place_type = "Restaurant"
            place_subtype = None  # Restaurant doesn't have a subtype field
        elif isinstance(place, StayPlace):
            place_type = "StayPlace"
            place_subtype = place.type
        elif isinstance(place, Cafe):
            place_type = "Cafe"
            place_subtype = None  # Cafe doesn't have a subtype field
        elif isinstance(place, TouristPlace):
            place_type = "TouristPlace"
            place_subtype = None
        elif isinstance(place, Mall):
            place_type = "Mall"
            place_subtype = None  # Mall doesn't have a subtype field
        elif isinstance(place, HealthCentre):
            place_type = "HealthCentre"
            place_subtype = place.type
        elif isinstance(place, HolyPlace):
            place_type = "HolyPlace"
            place_subtype = place.type
        elif isinstance(place, Financial):
            place_type = "Financial"
            place_subtype = place.type
        elif isinstance(place, GasStation):
            place_type = "GasStation"
            place_subtype = None  # GasStation doesn't have a subtype field
        elif isinstance(place, Entertainment):
            place_type = "Entertainment"
            place_subtype = None  # Entertainment doesn't have a subtype field
        elif isinstance(place, Sport):
            place_type = "Gym"
            place_subtype = Sport.type  # Gym doesn't have a subtype field
        elif isinstance(place, Salons):
            place_type = "Salons"
            place_subtype = place.type
        else:
            place_type = "PlaceMixin"  # Default type for the base class
            place_subtype = None  # Default subtype if not applicable

        return PlaceMixinOut(
            id=place.id,
            name=place.name,
            city=CityOut.from_orm(place.city),
            longitude=place.longitude,
            latitude=place.latitude,
            description=place.description,
            short_location=place.short_location,
            place_images=[PlaceImageOut.from_orm(image) for image in place.place_images],
            average_rating=place.average_rating,
            review_count=place.review_count,
            social_media=is_available,
            type=place_type,
            subtype=place_subtype,
            price=place.price,
            avaialble=place.available
        )


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


class ReviewsSchema(Schema):
    id: UUID4
    user: AccountOut
    place_id: UUID4
    comment: Optional[str]
    rating: int


class ReviewsIn(Schema):
    comment: Optional[str]
    rating: int


class AdvertisementSchema(Schema):
    id: UUID4
    country: CountryOut
    image: str
    title: str
    short_description: str
    url: str = None
    place: PlaceMixinOut = None

class OfferSchema(Schema):
    id: UUID4
    country: CountryOut
    image: str
    title: str
    short_description: str
    url: str = None
    place: PlaceMixinOut = None

class RecommendedPlacesOut(Schema):
    id: UUID4
    country: CountryOut
    place: PlaceMixinOut


class LatestPlacesOut(Schema):
    id: UUID4
    country: CountryOut
    place: PlaceMixinOut


class LatestPlacesCity(Schema):
    id: UUID4
    city: CityOut
    place: PlaceMixinOut


class FavoritePlaceOut(Schema):
    id: UUID4
    place: PlaceMixinOut


class CompanyOut(Schema):
    id: UUID4
    country: CountryOut
    company_name: str
    image: str  # Ensure that the field type is set to str
    company_description: str


class TripOut(Schema):
    id: UUID4
    trip_name: str
    short_description: str

class CompanyWithTripsOut(Schema):
    company: CompanyOut
    trips: List[TripOut]


class TripDetailOut(Schema):
    trip: TripOut
    trip_name: str
    trip_details: str
    social_media: SocialMediaSchema = None
    trip_images: List[PlaceImageOut] = None

