from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models import F, Q
from ninja import Router, File
from ninja.files import UploadedFile

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


@place_controller.get('/places/city/{city_id}', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def get_places_by_city_and_type(request, city_id: UUID4, place_type_name: str = None, type_name: str = None,
                                page: int = 1,
                                per_page: int = 10, sort_by_price: str = None):
    try:
        city = City.objects.get(id=city_id)
    except City.DoesNotExist:
        return 404, {'message': 'City not found.'}
    places = PlaceMixin.objects.filter(city=city)
    if place_type_name:
        places = places.filter(place_type__name=place_type_name)
    if type_name:
        places = places.filter(type__name=type_name)
    if sort_by_price == "low":
        places = places.order_by('price')
    elif sort_by_price == "high":
        places = places.order_by(F('price').desc())

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page)

    return 404, {'message': 'No places found.'}


@place_controller.get('/reviews/user', response={
    200: List[PlaceMixinOut],
    404: MessageOut
}, auth=AuthBearer())
def get_places_user_reviewed(request):
    user = request.auth

    if reviewed_places := PlaceMixin.objects.filter(reviews__user=user):
        return response(status.HTTP_200_OK, reviewed_places)
    else:
        return 404, {'message': 'No reviewed places found for the user.'}


# advertisement_controller = Router(tags=['Advertisement'])
#
#
# @advertisement_controller.get('/advertisement', response={
#     200: List[AdvertisementSchema],
#     404: MessageOut
# })
# def get_advertisement_by_country(request, country_id: UUID4, ):
#     if advertisement := Advertisement.objects.filter(country_id=country_id):
#         return response(status.HTTP_200_OK, advertisement)
#     return 404, {'message': 'No advertisement found.'}
#
#
# @advertisement_controller.get('/advertisement/city/{city_id}', response={
#     200: List[AdvertisementSchema],
#     404: MessageOut
# })
# def get_advertisement_by_city(request, city_id: UUID4):
#     if advertisement := Advertisement.objects.filter(city_id=city_id):
#         return response(status.HTTP_200_OK, advertisement)
#     return 404, {'message': 'No advertisement found.'}
#
#
# RecommendedPlaces_controller = Router(tags=['Recommended Places'])
#
#
# @RecommendedPlaces_controller.get('/recommended-places', response={
#     200: List[RecommendedPlacesOut],
#     404: MessageOut
# })
# def get_recommended_places_by_country(request, country_id: UUID4):
#     if recommended_places := RecommendedPlaces.objects.filter(
#             country_id=country_id
#     ):
#         return response(status.HTTP_200_OK, recommended_places)
#     return 404, {'message': 'No recommended places found.'}
#
#
# latest_places_controller = Router(tags=['Latest Places'])
#
#
# @latest_places_controller.get('/latest-places/country', response={
#     200: List[LatestPlacesOut],
#     404: MessageOut
# })
# def get_latest_places_by_country(request, country_id: UUID4):
#     try:
#         country = Country.objects.get(id=country_id)
#         if latest_places := LatestPlaces.objects.filter(
#                 country=country
#         ).order_by('-created')[:40]:
#             return response(status.HTTP_200_OK, latest_places)
#         return 404, {'message': 'No latest places found.'}
#     except Country.DoesNotExist:
#         return 404, {'message': 'Country not found.'}
#
#
# @latest_places_controller.get('/latest-places/city/{city_id}', response={
#     200: List[LatestPlacesCity],
#     404: MessageOut
# })
# def get_latest_places_by_city(request, city_id: UUID4):
#     try:
#         city = City.objects.get(id=city_id)
#         if latest_places := LatestPlaces.objects.filter(
#                 city=city
#         ).order_by('-created')[:40]:
#             return response(status.HTTP_200_OK, latest_places)
#         return 404, {'message': 'No latest places found.'}
#     except City.DoesNotExist:
#         return 404, {'message': 'City not found.'}


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
def get_reviews_by_place(request, place_id: UUID4, user_id: UUID4):
    try:
        reviews = Reviews.objects.filter(place_id=place_id)

        if not reviews.exists():
            return 404, {'message': 'No reviews found for the specified place.'}

        if user_review := reviews.filter(user_id=user_id).first():
            # If the user has a review, put it at the beginning of the list
            reviews = [user_review] + [review for review in reviews if review != user_review]
        else:
            reviews = reviews.order_by('-created')

        return reviews

    except Reviews.DoesNotExist:
        return 404, {'message': 'Place not found.'}


@review_controller.post('/', response={200: ReviewsIn, 404: MessageOut}, auth=AuthBearer())
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
    return response(status.HTTP_200_OK, review)


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


# @search_controller.get('/places/search', response={
#     200: PlaceMixinSchema,
#     404: MessageOut
# })
# def search_places(request, country_id: UUID4, search: str, city_id: UUID4 = None, place_type: str = None,
#                   per_page: int = 10, page: int = 1):
#     try:
#         country = Country.objects.get(id=country_id)
#     except Country.DoesNotExist:
#         return 404, {'message': 'Country not found.'}
#
#     places = PlaceMixin.objects.filter(city__country=country)
#
#     if city_id:
#         places = places.filter(city_id=city_id)
#
#     if search:
#         places = places.filter(name__icontains=search)
#
#     if place_type:
#         if filtered_places := filter_by_place_type(places, place_type):
#             return response(status.HTTP_200_OK, filtered_places, paginated=True, per_page=per_page, page=page, )
#         else:
#             return 404, {'message': 'No places found for the specified type.'}
#
#     if places:
#         return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page, )
#
#     return 404, {'message': 'No places found.'}

@search_controller.get('/places/search', response={
    200: PlaceMixinSchema,
    404: MessageOut
})
def search_places(request, country_id: UUID4, search: str, city_id: UUID4 = None, place_type_name: str = None,
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

    if place_type_name:
        places = places.filter(place_type__name=place_type_name)

    if places:
        return response(status.HTTP_200_OK, places, paginated=True, per_page=per_page, page=page, )

    return 404, {'message': 'No places found.'}


trip_controller = Router(tags=['Trips'])


@trip_controller.get('/company/{company_id}', response={
    200: CompanyWithTripsOut,
    404: MessageOut
})
def get_trips_by_company(request, company_id: UUID4):
    try:
        company = Company.objects.get(id=company_id)
        trips = Trip.objects.filter(company_id=company_id)

        if not trips.exists():
            return 404, {'message': 'No trips found for the specified company.'}

        trip_out_list = [TripOut.from_orm(trip) for trip in trips]
        trip_detail_out_list = []

        for trip in trips:
            trip_details = TripDetails.objects.filter(trip_id=trip.id)
            if trip_details.exists():
                trip_detail_out_list.extend([TripDetailOut.from_orm(detail) for detail in trip_details])

        company_out = CompanyOut(
            id=company.id,
            city=CityOut.from_orm(company.city),  # Set the city field with CityOut object
            company_name=company.company_name,
            image=str(company.image),  # Ensure that the image is converted to str
            company_description=company.company_description,
        )

        company_with_trips_out = CompanyWithTripsOut(
            company=company_out,
            trips=trip_out_list,
            trip_details=trip_detail_out_list
        )

        return response(status.HTTP_200_OK, company_with_trips_out)
    except Company.DoesNotExist:
        return 404, {'message': 'Company not found.'}




@trip_controller.get('/companies/{city_name}', response={
    200: List[CompanyOut],
    404: MessageOut
})
def get_companies_by_city_name(request, city_name: str):
    try:
        companies = Company.get_companies_by_city_name(city_name)

        if not companies.exists():
            return 404, {'message': 'No companies found for the specified city.'}

        company_out_list = [CompanyOut(
            id=company.id,
            city=CityOut.from_orm(company.city),
            company_name=company.company_name,
            image=str(company.image),
            company_description=company.company_description,
        ) for company in companies]

        return response(status.HTTP_200_OK, company_out_list)
    except City.DoesNotExist:
        return 404, {'message': 'City not found.'}


merchant_controller = Router(tags=['Merchants'])


@merchant_controller.post('/places', response={200: PlaceMixinOut, 404: MessageOut, 403: MessageOut}, auth=AuthBearer())
def add_place_by_merchant(request, place_data: PlaceCreate, images: List[UploadedFile] = File(...)):
    user = request.auth
    try:
        user = EmailAccount.objects.get(id=place_data.user_id)
    except EmailAccount.DoesNotExist:
        return 404, {'message': 'Merchant not found.'}
    if PlaceMixin.objects.filter(user=user).exists():
        return 403, {'message': 'Merchant can only add one place.'}
    try:
        city = City.objects.get(id=place_data.city_id)
    except City.DoesNotExist:
        return 404, {'message': 'City not found.'}

    place_type = PlaceType.objects.get(name=place_data.place_type)

    if not place_type:
        return 404, {'message': 'Invalid place type'}

    # place_subtype = PlaceSubType.objects.get(name=place_data.type)
    if place_data.type:
        place_subtype = PlaceSubType.objects.get(name=place_data.type)
    else:
        place_subtype = None
    if not user.is_merchant and not user.is_free:
        return 403, {'message': 'Only merchants can add places.'}

    place = PlaceMixin.objects.create(
        user=user,
        name=place_data.name,
        city=city,
        place_type=place_type,
        type=place_subtype,
        location=place_data.location,
        description=place_data.description,
        short_location=place_data.short_location,
        price=place_data.price,
        open=place_data.open,
        phone_number=place_data.phone_number,
    )

    for image in images:
        place_image = Images(place=place, image=image)
        place_image.save()

    social_media = SocialMedia.objects.create(
        facebook=place_data.facebook,
        instagram=place_data.instagram,
        telegram=place_data.telegram,
        whatsapp=place_data.whatsapp,
    )
    place.social_media = social_media

    social_media.save()
    place.save()

    return response(status.HTTP_200_OK, PlaceMixinOut.from_orm(place))


@merchant_controller.get('/merchant/place', response={200: PlaceMixinOut, 404: MessageOut}, auth=AuthBearer())
def get_merchant_place(request):
    user = request.auth
    try:
        user = EmailAccount.objects.get(id=user.id)
    except EmailAccount.DoesNotExist:
        return 404, {'message': 'Merchant not found.'}
    if not user.is_merchant and not user.is_free:
        return 404, {'message': 'Merchant not found.'}
    try:
        place = PlaceMixin.objects.get(user=user)
        return response(status.HTTP_200_OK, PlaceMixinOut.from_orm(place))
    except PlaceMixin.DoesNotExist:
        return 404, {'message': 'Place not found.'}


@merchant_controller.put('/merchant/place/edit', response={200: PlaceMixinOut, 404: MessageOut}, auth=AuthBearer())
def edit_merchant_place(request, place_data: PlaceUpdate,
                        ):
    user = request.auth
    try:
        user = EmailAccount.objects.get(id=user.id)
    except EmailAccount.DoesNotExist:
        return 404, {'message': 'Account not found.'}
    if not user.is_merchant and not user.is_free:
        return 404, {'message': 'Merchant not found.'}
    try:
        place = PlaceMixin.objects.get(user=user)
        social_media = SocialMedia.objects.get(id=place.social_media.id)
        social_media.facebook = place_data.facebook
        social_media.instagram = place_data.instagram
        social_media.telegram = place_data.telegram
        social_media.whatsapp = place_data.whatsapp
        social_media.save()

        place.name = place_data.name
        place.description = place_data.description
        place.price = place_data.price
        place.open = place_data.open
        place.phone_number = place_data.phone_number

        place.save()

        # if images:
        #     for image in images:
        #         place_image = Images(place=place, image=image)
        #         place_image.save()

        return response(status.HTTP_200_OK, PlaceMixinOut.from_orm(place))
    except PlaceMixin.DoesNotExist:
        return 404, {'message': 'Place not found.'}

