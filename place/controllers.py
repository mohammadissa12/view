from ninja import Router
from django.db.models import Q

from account.models import EmailAccount
from conf.utils import status
from conf.utils.permissions import AuthBearer
from conf.utils.schemas import MessageOut
from conf.utils.utils import response
from location.models import City, Country
from .models import *
from .schemas import *

place_controller = Router(tags=['Places'])


@place_controller.get('/reviews/{place_id}', response={
    200: List[ReviewsSchema],
    404: MessageOut
})
def get_reviews_by_place(request, place_id: UUID4):
    try:
        reviews = Reviews.objects.filter(place_id=place_id)
        if reviews:
            return response(status.HTTP_200_OK, reviews)
        return 404, {'message': 'No reviews found for the specified place.'}
    except Reviews.DoesNotExist:
        return 404, {'message': 'Place not found.'}






@place_controller.get('/places/{pk}', response={
    200: PlaceMixinOut,
    404: MessageOut
})
def get_place(request, pk: UUID4):
    try:
        place = PlaceMixin.objects.get(id=pk)
        return place
    except PlaceMixin.DoesNotExist:
        return 404, {'message': 'Place not found.'}


def get_places_by_city(city_id: UUID4, place_model):
    try:
        city = City.objects.get(id=city_id)
        places = place_model.objects.filter(city=city)
        return places
    except City.DoesNotExist:
        return None


@place_controller.get('/restaurants/city', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_restaurant_by_city(request, city_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    places = get_places_by_city(city_id, Restaurant)
    if places is None:
        return 404, {'message': 'City not found.'}

    if search:
        places = places.filter(name__icontains=search)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No restaurants found.'}


@place_controller.get('/stayplace/city', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_stay_place_by_city(request, city_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    places = get_places_by_city(city_id, StayPlace)
    if places is None:
        return 404, {'message': 'City not found.'}

    if search:
        places = places.filter(name__icontains=search)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No stay places found.'}


@place_controller.get('/cafeteria/city', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_cafeteria_by_city(request, city_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    places = get_places_by_city(city_id, Cafe)
    if places is None:
        return 404, {'message': 'City not found.'}

    if search:
        places = places.filter(name__icontains=search)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No cafeterias found.'}


@place_controller.get('/tourist-place/city', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_tourist_place_by_city(request, city_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    places = get_places_by_city(city_id, TouristPlace)
    if places is None:
        return 404, {'message': 'City not found.'}

    if search:
        places = places.filter(name__icontains=search)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No tourist places found.'}


@place_controller.get('/malls/city', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_mall_by_city(request, city_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    places = get_places_by_city(city_id, Mall)
    if places is None:
        return 404, {'message': 'City not found.'}

    if search:
        places = places.filter(name__icontains=search)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No malls found.'}


@place_controller.get('/healthcare-center/city', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_healthcare_center_by_city(request, city_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    places = get_places_by_city(city_id, HealthCentre)
    if places is None:
        return 404, {'message': 'City not found.'}

    if search:
        places = places.filter(name__icontains=search)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No healthcare centers found.'}


@place_controller.get('/holy-places/city', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_holy_places_by_city(request, city_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    places = get_places_by_city(city_id, HolyPlace)
    if places is None:
        return 404, {'message': 'City not found.'}

    if search:
        places = places.filter(name__icontains=search)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No holy places centers found.'}


@place_controller.get('/financial/city', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_financial_by_city(request, city_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    places = get_places_by_city(city_id, Financial)
    if places is None:
        return 404, {'message': 'City not found.'}

    if search:
        places = places.filter(name__icontains=search)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No financial places found.'}


@place_controller.get('/gas-station/city', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_gas_station_by_city(request, city_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    places = get_places_by_city(city_id, GasStation)
    if places is None:
        return 404, {'message': 'City not found.'}

    if search:
        places = places.filter(name__icontains=search)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No gas station found.'}


@place_controller.get('/entertainment/city', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_entertainment_by_city(request, city_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    places = get_places_by_city(city_id, Entertainment)
    if places is None:
        return 404, {'message': 'City not found.'}

    if search:
        places = places.filter(name__icontains=search)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No Entertainment places found.'}


@place_controller.get('/gym/city', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_gym_by_city(request, city_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    places = get_places_by_city(city_id, Gym)
    if places is None:
        return 404, {'message': 'City not found.'}

    if search:
        places = places.filter(name__icontains=search)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No gym places found.'}


@place_controller.get('/salon/city', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_salon_by_city(request, city_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    places = get_places_by_city(city_id, Salons)
    if places is None:
        return 404, {'message': 'City not found.'}

    if search:
        places = places.filter(name__icontains=search)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No salon places found.'}


advertisement_controller = Router(tags=['Advertisement'])


@advertisement_controller.get('/advertisement', response={
    200: List[AdvertisementSchema],
    404: MessageOut
})
def get_advertisement_by_country(request, country_id: UUID4, ):
    advertisement = Advertisement.objects.filter(country_id=country_id)
    if advertisement:
        return response(status.HTTP_200_OK, advertisement)
    return 404, {'message': 'No advertisement found.'}


@advertisement_controller.get('/advertisement/content_type/{model}', response={
    200: List[AdvertisementSchema],
    404: MessageOut
})
def get_advertisement_by_content_type(request, model: str):
    try:
        content_type = ContentType.objects.get(model=model)
    except ContentType.DoesNotExist:
        return 404, {'message': 'Content type not found.'}

    advertisements = Advertisement.objects.filter(content_type=content_type)
    if advertisements:
        return response(status.HTTP_200_OK, advertisements)
    return 404, {'message': 'No advertisement found for the specified content type.'}


RecommendedPlaces_controller = Router(tags=['Recommended Places'])


@RecommendedPlaces_controller.get('/recommended-places', response={
    200: List[RecommendedPlacesOut],
    404: MessageOut
})
def get_recommended_places_by_country(request, country_id: UUID4):
    recommended_places = RecommendedPlaces.objects.filter(country_id=country_id)
    if recommended_places:
        return response(status.HTTP_200_OK, recommended_places)
    return 404, {'message': 'No recommended places found.'}


latest_places_controller = Router(tags=['Latest Places'])


@latest_places_controller.get('/latest-places/country', response={
    200: List[LatestPlacesOut],
    404: MessageOut
})
def get_latest_places_by_country(request, country_id: UUID4):
    try:
        country = Country.objects.get(id=country_id)
        latest_places = LatestPlaces.objects.filter(country=country).order_by('-created')[:5]
        if latest_places:
            return response(status.HTTP_200_OK, latest_places)
        return 404, {'message': 'No latest places found.'}
    except Country.DoesNotExist:
        return 404, {'message': 'Country not found.'}


favorite_places_controller = Router(tags=['favorite places'])


@favorite_places_controller.get('all', auth=AuthBearer(), response={
    200: List[FavoritePlaceOut],
    404: MessageOut

})
def get_favorite_places(request):
    user = request.auth
    favorite_places_qs = user.favorite_places.all()
    if favorite_places_qs:
        return response(status.HTTP_200_OK, favorite_places_qs)
    return 404, {'message': 'No favorite places found.'}


# add
@favorite_places_controller.post('add', auth=AuthBearer(), response={
    200: FavoritePlaceOut,
    404: MessageOut
})
def add_favorite_place(request, place_id: UUID4):
    user = request.auth
    try:
        place = PlaceMixin.objects.get(id=place_id)
        favorite_place, created = FavoritePlaces.objects.get_or_create(user=user, place=place)
        if created:
            return response(status.HTTP_200_OK, favorite_place)
        return 404, {'message': 'Place already added to favorite.'}
    except PlaceMixin.DoesNotExist:
        return 404, {'message': 'Place not found.'}


# remove


@favorite_places_controller.delete('remove', auth=AuthBearer(), response={
    202: MessageOut,
    404: MessageOut
})
def remove_favorite_place(request, place_id: UUID4):
    user = request.auth
    place = PlaceMixin.objects.get(id=place_id)
    if place:
        favorite_place = user.favorite_places.filter(place=place).delete()
        return response(status.HTTP_202_ACCEPTED, {'message': 'Place removed from favorite.'})

    return 404, {'message': 'Place not found.'}


