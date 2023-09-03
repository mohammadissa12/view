from django.db.models import Q
from django.shortcuts import get_object_or_404
from ninja import Router
from pydantic import UUID4
from typing import List

from conf.utils import status
from conf.utils.schemas import MessageOut
from conf.utils.utils import response
from place.models import Advertisement, LatestPlaces, RecommendedPlaces
from place.schemas import AdvertisementSchema, RecommendedPlacesOut, LatestPlacesOut
from .models import Country, City
from .schemas import *
from .schemas2 import CountrySchema2, CitySchema2

country_controller = Router(tags=['Location'])


@country_controller.get('/countries', response={
    200: CountrySchema,
    404: MessageOut
})
def all_countries(request, search=None, per_page: int = 12, page: int = 1):
    if search:
        countries = Country.objects.filter(
            Q(country_name__icontains=search))
    else:
        countries = Country.objects.all()
    if countries:
        return response(status.HTTP_200_OK, countries, paginated=True, per_page=per_page, page=page)
    return 404, {'message': 'No countries found.'}


@country_controller.get('/countries/{country_name}', response={
    200: CountryOut,
    404: MessageOut
})
def get_country(request, country_name: str):
    try:
        return get_object_or_404(Country, country_name__iexact=country_name)
    except Country.DoesNotExist:
        return 404, {'message': 'Country not found.'}


#
@country_controller.get('/cities/{city_id}', response={
    200: CityOut,
    404: MessageOut})
def get_city(request, city_id: UUID4):
    try:
        return City.objects.get(id=city_id)
    except City.DoesNotExist:
        return 404, {'message': 'City not found.'}


@country_controller.get('/cites/{country_name}', response={
    200: List[City2],
    404: MessageOut
})
def get_cities_by_country(request, country_name: str):
    try:
        country = Country.objects.get(country_name__iexact=country_name)
        cities = City.objects.filter(country=country)
        if cities:
            return response(status.HTTP_200_OK, cities,)
        return 404, {'message': 'No cities found.'}
    except Country.DoesNotExist:
        return 404, {'message': 'Country not found.'}


@country_controller.get('/country/{country_name}', response={
    200: CountrySchema2,
    404: MessageOut
})
def get_country_by_name(request, country_name: str):
    try:
        return get_object_or_404(Country, country_name__iexact=country_name)
    except Country.DoesNotExist:
        return 404, {'message': 'Country not found.'}


@country_controller.get('/city', response={
    200: CitySchema2,
    404: MessageOut
})
def get_city_by_id(request, city_id: UUID4):
    try:
        return get_object_or_404(City, id=city_id)
    except City.DoesNotExist:
        return 404, {'message': 'City not found.'}

