from ninja import Router

from account.models import EmailAccount
from conf.utils import status
from conf.utils.permissions import AuthBearer
from conf.utils.schemas import MessageOut
from conf.utils.utils import response
from location.models import City, Country
from .models import *
from .schemas import *


def filter_by_place_type(places, place_type):
    if place_type.lower() == 'restaurant':
        return Restaurant.objects.filter(id__in=places.values('id'))
    elif place_type.lower() == 'stayplace':
        return StayPlace.objects.filter(id__in=places.values('id'))
    elif place_type.lower() == 'cafe':
        return Cafe.objects.filter(id__in=places.values('id'))
    elif place_type.lower() == 'touristplace':
        return TouristPlace.objects.filter(id__in=places.values('id'))
    elif place_type.lower() == 'mall':
        return Mall.objects.filter(id__in=places.values('id'))
    elif place_type.lower() == 'healthcentre':
        return HealthCentre.objects.filter(id__in=places.values('id'))
    elif place_type.lower() == 'holyplace':
        return HolyPlace.objects.filter(id__in=places.values('id'))
    elif place_type.lower() == 'financial':
        return Financial.objects.filter(id__in=places.values('id'))
    elif place_type.lower() == 'gasstation':
        return GasStation.objects.filter(id__in=places.values('id'))
    elif place_type.lower() == 'entertainment':
        return Entertainment.objects.filter(id__in=places.values('id'))
    elif place_type.lower() == 'gym':
        return Gym.objects.filter(id__in=places.values('id'))
    elif place_type.lower() == 'salons':
        return Salons.objects.filter(id__in=places.values('id'))
    else:
        return None


place_controller = Router(tags=['Places'])


@place_controller.get('/places/{pk}', response={
    200: PlaceMixinOut,
    404: MessageOut
})
def get_place(request, pk: UUID4):
    try:
        return PlaceMixin.objects.get(id=pk)
    except PlaceMixin.DoesNotExist:
        return 404, {'message': 'Place not found.'}


def get_places_by_city(city_id: UUID4, place_model):
    try:
        city = City.objects.get(id=city_id)
        return place_model.objects.filter(city=city)
    except City.DoesNotExist:
        return None


@place_controller.get('/places/city/{pk}', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_places_by_city(request, city_id: UUID4, place_type: str, page: int = 1, per_page: int = 10):
    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        return 404, {'message': 'City not found.'}

    places = PlaceMixin.objects.filter(city=city)

    if place_type:
        if filtered_places := filter_by_place_type(places, place_type):
            return response(status.HTTP_200_OK, filtered_places, paginated=True, per_page=per_page, page=page, )
        else:
            return 404, {'message': 'No places found for the specified type.'}

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, page=page, per_page=per_page, )
    return 404, {'message': 'No places found.'}


advertisement_controller = Router(tags=['Advertisement'])


@advertisement_controller.get('/advertisement', response={
    200: List[AdvertisementSchema],
    404: MessageOut
})
def get_advertisement_by_country(request, country_id: UUID4, ):
    if advertisement := Advertisement.objects.filter(country_id=country_id):
        return response(status.HTTP_200_OK, advertisement)
    return 404, {'message': 'No advertisement found.'}


@advertisement_controller.get('/advertisement/content_type/{model}/{country_id}', response={
    200: List[AdvertisementSchema],
    404: MessageOut
})
def get_advertisement_by_content_type(request, model: str, country_id: UUID4):
    try:
        content_type = ContentType.objects.get(model=model)
    except ContentType.DoesNotExist:
        return 404, {'message': 'Content type not found.'}

    try:
        country = Country.objects.get(id=country_id)
    except Country.DoesNotExist:
        return 404, {'message': 'Country not found.'}

    if advertisements := Advertisement.objects.filter(content_type=content_type, country=country):
        return response(status.HTTP_200_OK, advertisements)

    return 404, {'message': 'No advertisements found for the specified content type and country.'}


RecommendedPlaces_controller = Router(tags=['Recommended Places'])


@RecommendedPlaces_controller.get('/recommended-places', response={
    200: List[RecommendedPlacesOut],
    404: MessageOut
})
def get_recommended_places_by_country(request, country_id: UUID4):
    if recommended_places := RecommendedPlaces.objects.filter(
            country_id=country_id
    ):
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
        if latest_places := LatestPlaces.objects.filter(
                country=country
        ).order_by('-created')[:5]:
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
    if favorite_places_qs := user.favorite_places.all():
        return response(status.HTTP_200_OK, favorite_places_qs)
    return 404, {'message': 'No favorite places found.'}


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


@favorite_places_controller.delete('remove', auth=AuthBearer(), response={
    202: MessageOut,
    404: MessageOut
})
def remove_favorite_place(request, place_id: UUID4):
    user = request.auth
    if place := PlaceMixin.objects.get(id=place_id):
        favorite_place = user.favorite_places.filter(place=place).delete()
        return response(status.HTTP_202_ACCEPTED, {'message': 'Place removed from favorite.'})

    return 404, {'message': 'Place not found.'}


review_controller = Router(tags=['Reviews'])


@review_controller.get('/reviews/{place_id}', response={
    200: List[ReviewsSchema],
    404: MessageOut
})
def get_reviews_by_place(request, place_id: UUID4):
    try:
        if reviews := Reviews.objects.filter(place_id=place_id):
            return response(status.HTTP_200_OK, reviews)
        return 404, {'message': 'No reviews found for the specified place.'}
    except Reviews.DoesNotExist:
        return 404, {'message': 'Place not found.'}


@review_controller.post('/', response={201: ReviewsIn, 404: MessageOut}, auth=AuthBearer())
def create_review(request, review_data: ReviewsIn, place_id: UUID4):
    user = request.auth

    try:
        place = PlaceMixin.objects.get(id=place_id)
    except PlaceMixin.DoesNotExist:
        return 404, {'message': 'Place not found.'}

    review = Reviews.objects.create(
        user=user,
        place=place,
        comment=review_data.comment,
        rating=review_data.rating
    )
    return response(status.HTTP_201_CREATED, review)


@review_controller.delete('/remove', response={200: MessageOut, 404: MessageOut}, auth=AuthBearer())
def delete_review(request, review_id: UUID4):
    user = request.auth

    try:
        review = Reviews.objects.get(id=review_id)
    except Reviews.DoesNotExist:
        return 404, {'message': 'Review not found.'}
    print(review.user, user)
    if review.user != user:
        return 403, {'message': 'You are not allowed to delete this review.'}

    review.delete()
    return response(status.HTTP_200_OK, {'message': 'Review deleted successfully.'})


@review_controller.post(('/comments/{comment_id}/report'), response={200: MessageOut, 404: MessageOut},
                        auth=AuthBearer())
def report_comment(request, comment_id: UUID4):
    user = request.auth

    try:
        comment = Reviews.objects.get(id=comment_id)
    except Reviews.DoesNotExist:
        return 404, {'message': 'Comment not found.'}

    if comment.user == user:
        return 403, {'message': 'You are not allowed to report your own comment.'}

    comment.reported = True
    comment.save()
    return response(status.HTTP_200_OK, {'message': 'Comment reported successfully.'})


search_controller = Router(tags=['Search'])


@search_controller.get('/places/search/{pk}', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def search_places(request, country_id: UUID4, search: str, city_id: UUID4 = None, place_type: str = None,
                  per_page: int = 10, page: int = 1):
    try:
        country = Country.objects.get(id=country_id)
    except Country.DoesNotExist:
        return 404, {'message': 'Country not found.'}

    places = PlaceMixin.objects.filter(city__country=country)

    if city_id:
        places = places.filter(city_id=city_id)

    if search:
        places = places.filter(name__icontains=search)

    if place_type:
        if filtered_places := filter_by_place_type(places, place_type):
            return response(status.HTTP_200_OK, filtered_places, paginated=True, per_page=per_page, page=page,)
        else:
            return 404, {'message': 'No places found for the specified type.'}

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page, )

    return 404, {'message': 'No places found.'}
