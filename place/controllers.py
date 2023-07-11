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


@place_controller.get('/places/{pk}', response={
    200: PlaceOut,
    404: MessageOut
})
def get_place(request, pk: UUID4):
    try:
        place = PlaceMixin.objects.get(id=pk)
        return place
    except PlaceMixin.DoesNotExist:
        return 404, {'message': 'Place not found.'}


@place_controller.get('/places/city/{city_id}/place_type/{place_type}', response={
    200: PlaceSchema,
    404: MessageOut
})
def get_places_by_city_and_place_type(request, city_id: UUID4, place_type: str, page: int = 1, per_page: int = 200):
    try:
        city = City.objects.get(id=city_id)
        places = PlaceMixin.objects.filter(city=city, place_type=place_type)
        if places:
            return response(status.HTTP_200_OK, places, paginated=True, page=page, per_page=per_page)
        return 404, {'message': 'No places found.'}
    except City.DoesNotExist:
        return 404, {'message': 'City not found.'}


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


@advertisement_controller.get('/advertisement/place_type', response={
    200: List[AdvertisementSchema],
    404: MessageOut
})
def get_advertisement_by_country_and_place_type(request, country_id: UUID4, place_type: str):
    advertisement = Advertisement.objects.filter(country_id=country_id, place_type=place_type)
    if advertisement:
        return response(status.HTTP_200_OK, advertisement)
    return 404, {'message': 'No advertisement found.'}


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

