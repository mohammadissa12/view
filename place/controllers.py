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

@place_controller.get('/places/{place_id}/nearest/', response={
    200: List[PlaceMixinOut],
    404: MessageOut  # You might need to import the MessageOut schema if not already imported
})
def get_nearest_places(request, place_id: UUID4):
    try:
        specific_place = PlaceMixin.objects.get(id=place_id)
    except PlaceMixin.DoesNotExist:
        return 404, {'message': 'Place not found.'}

    # Get the list of nearest places
    nearest_places = specific_place.get_nearest_places()

    # Convert the nearest places to the PlaceMixinOut schema
    nearest_places_output = [PlaceMixinOut.from_orm(place) for place in nearest_places]

    return response(status.HTTP_200_OK, nearest_places_output)

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

@review_controller.get("/reviews", response={200: List[ReviewSchema],400:MessageOut})
def get_reviews(
    request,
    entity_type: str,
    place_id: UUID4 = None,
    company_id: UUID4 = None,
    user_id: UUID4 = None
):
    if entity_type not in ["place", "company"]:
        return response(status.HTTP_400_BAD_REQUEST, {"message": "Invalid entity_type."})

    if place_id is None and company_id is None:
        return response(status.HTTP_400_BAD_REQUEST, {"message": "Either place_id or company_id should be provided."})

    filters = {"entity_type": entity_type}
    if place_id:
        filters["place_id"] = place_id
    if company_id:
        filters["company_id"] = company_id
    reviews = Reviews.objects.filter(**filters)

    review_list = []

    if user_id and place_id:
        user_review = Reviews.objects.filter(user_id=user_id, place_id=place_id).first()
        if user_review:
            user_review_data = {
                "id": user_review.id,
                "user": user_review.user,
                "place_id": user_review.place_id,
                "company_id": user_review.company_id,
                "entity_type": user_review.entity_type,
                "comment": user_review.comment,
                "rating": user_review.rating,
            }
            review_list.append(user_review_data)
    # Order the remaining reviews by 'created' in descending order
    other_reviews = reviews.exclude(user_id=user_id).order_by('-created')
    for review in other_reviews:
        review_data = {
            "id": review.id,
            "user": review.user,
            "place_id": review.place_id,
            "company_id": review.company_id,
            "entity_type": review.entity_type,
            "comment": review.comment,
            "rating": review.rating,
        }
        review_list.append(review_data)

    return review_list


@review_controller.post('/add', response={200: ReviewsIn, 404: MessageOut}, auth=AuthBearer())
def add_review(request, review_data: ReviewsIn,place_id: UUID4 = None, company_id: UUID4 = None,entity_type: str = None):
    user = request.auth
    try:
        if entity_type == "place":
            place = PlaceMixin.objects.get(id=place_id)
            review = Reviews.objects.create(
                user=user,
                place=place,
                entity_type=entity_type,
                comment=review_data.comment,
                rating=review_data.rating
            )
            return response(status.HTTP_200_OK, ReviewSchema.from_orm(review))
        elif entity_type == "company":
            company = Company.objects.get(id=company_id)
            review = Reviews.objects.create(
                user=user,
                company=company,
                entity_type=entity_type,
                comment=review_data.comment,
                rating=review_data.rating
            )
            return response(status.HTTP_200_OK, ReviewSchema.from_orm(review))
        else:
            return response(status.HTTP_400_BAD_REQUEST, {"message": "Invalid entity_type."})
    except PlaceMixin.DoesNotExist:
        return 404, {'message': 'Place not found.'}
    except Company.DoesNotExist:
        return 404, {'message': 'Company not found.'}


@review_controller.delete("/delete", response={200: MessageOut, 403: MessageOut}, auth=AuthBearer())
def delete_review(
    request,
    review_id: UUID4
):
    user = request.auth
    try:
        review = Reviews.objects.get(id=review_id)
        if user == review.user:
            review.delete()
            return response(status.HTTP_200_OK, {"message": "Review deleted successfully."})
        else:
            return response(status.HTTP_403_FORBIDDEN, {"message": "You are not allowed to delete this review."})

    except Reviews.DoesNotExist:
        return 404, {'message': 'Review not found.'}


@review_controller.post("/report", response={200: MessageOut, 404: MessageOut}, auth=AuthBearer())
def report_review(
    request,
    review_id: UUID4
):
    user = request.auth
    try:
        review = Reviews.objects.get(id=review_id)

        # Check if the user is the author of the review or has appropriate permissions to report
        if user == review.user:
            return response(status.HTTP_403_FORBIDDEN, {"message": "You cannot report your own review."})

        # Check if the review is already reported
        if review.reported:
            return response(status.HTTP_200_OK, {"message": "Review has already been reported."})

        # Mark the review as reported
        review.reported = True
        review.save()

        return response(status.HTTP_200_OK, {"message": "Review reported successfully."})

    except Reviews.DoesNotExist:
        return 404, {'message': 'Review not found.'}


search_controller = Router(tags=['Search'])


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
        trips = TripDetails.objects.filter(company_id=company_id)

        if not trips.exists():
            return 404, {'message': 'No trips found for the specified company.'}

        trip_detail_out_list = []
        for trip in trips:
            trip_detail_out = TripDetailOut(
                id=trip.id,
                trip_name=trip.trip_name,
                short_description=trip.short_description,
                trip_details=trip.trip_details,
                trip_images=[PlaceImageOut.from_orm(image) for image in trip.trip_images],
            )
            trip_detail_out_list.append(trip_detail_out)

        company_out = CompanyOut(
            id=company.id,
            city=CityOut.from_orm(company.city),
            company_name=company.company_name,
            image=str(company.image),  # Ensure that the image is converted to str
            latitude=company.latitude,
            longitude=company.longitude,
            company_description=company.company_description,
            social_media=company.social_media_company,
        )

        company_with_trips_out = CompanyWithTripsOut(
            company=company_out,
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
        # Fetch companies queryset (multiple companies)
        companies = Company.get_companies_by_city_name(city_name)

        if not companies.exists():
            return 404, {'message': 'No companies found for the specified city.'}

        # Create a list of CompanyOut instances
        company_out_list = []
        for company in companies:
            # Retrieve the associated SocialMedia data for each company
            social_media = company.get_social_media
            # Create a CompanyOut instance
            company_out = CompanyOut(
                id=company.id,
                city=CityOut.from_orm(company.city),
                company_name=company.company_name,
                image=company.image_url,
                company_description=company.company_description,
                longitude=company.longitude,
                latitude=company.latitude,
                social_media=social_media,
                average_rating=company.average_rating,
                review_count=company.review_count,
            )
            company_out_list.append(company_out)

        return response(status.HTTP_200_OK, company_out_list)

    except Company.DoesNotExist:
        return 404, {'message': 'Company not found.'}


merchant_controller = Router(tags=['Merchants'])


@merchant_controller.post('/places', response={200: PlaceMixinOut, 404: MessageOut, 403: MessageOut}, auth=AuthBearer())
def add_place_by_merchant(request, place_data: PlaceCreate):
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

        return response(status.HTTP_200_OK, PlaceMixinOut.from_orm(place))
    except PlaceMixin.DoesNotExist:
        return 404, {'message': 'Place not found.'}


@merchant_controller.post('/places/images', response={200: PlaceMixinOut, 404: MessageOut, 403: MessageOut}, auth=AuthBearer())
def add_place_images_by_merchant(request, place_id: UUID4, images: List[UploadedFile] = File(...)):
    try:
        place = PlaceMixin.objects.get(id=place_id)
    except PlaceMixin.DoesNotExist:
        return 404, {'message': 'Place not found.'}

    user = request.auth
    if place.user != user:
        return 403, {'message': 'You do not have permission to add images for this place.'}

    for image in images:
        place_image = Images(place=place, image=image)
        place_image.save()

    return response(status.HTTP_200_OK, PlaceMixinOut.from_orm(place))


@merchant_controller.delete('/places/images/{image_id}', response={200: MessageOut, 404: MessageOut, 403: MessageOut}, auth=AuthBearer())
def delete_place_image_by_merchant(request, image_id: UUID4):
    try:
        image = Images.objects.get(id=image_id)
    except Images.DoesNotExist:
        return 404, {'message': 'Image not found.'}

    place = image.place
    user = request.auth
    if place.user != user:
        return 403, {'message': 'You do not have permission to delete images for this place.'}

    image.delete()

    return response(status.HTTP_200_OK, {'message': 'Image deleted successfully.'})


@merchant_controller.get('/merchant/place/images', response={200: List[PlaceImageOut], 404: MessageOut}, auth=AuthBearer())
def get_merchant_place_images(request):
    user = request.auth
    try:
        user = EmailAccount.objects.get(id=user.id)
    except EmailAccount.DoesNotExist:
        return 404, {'message': 'Account not found.'}
    if not user.is_merchant :
        return 404, {'message': 'Merchant not found.'}
    try:
        place = PlaceMixin.objects.get(user=user)
        return response(status.HTTP_200_OK, [PlaceImageOut.from_orm(image) for image in place.place_images])
    except PlaceMixin.DoesNotExist:
        return 404, {'message': 'Place not found.'}


#return social media of company
@merchant_controller.get('/company/social_media', response={200: SocialMediaSchema, 404: MessageOut})
def get_company_social_media(request, company_id: UUID4):
    try:
        company = Company.objects.get(id=company_id)
        print(company.social_media_company)
        return response(status.HTTP_200_OK, SocialMediaSchema.from_orm(company.social_media_company))
    except Company.DoesNotExist:
        return 404, {'message': 'Company not found.'}