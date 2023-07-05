from django.db.models import Q
from ninja import Router
from pydantic import UUID4
from typing import List

from conf.utils import status
from conf.utils.schemas import MessageOut
from conf.utils.utils import response
from .models import Country, City
from .schemas import *

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


@country_controller.get('/countries/{pk}', response={
    200: CountryOut,
    404: MessageOut
})
def get_country(request, pk: UUID4):
    try:
        country = Country.objects.get(id=pk)
        return country
    except Country.DoesNotExist:
        return 404, {'message': 'Country not found.'}


#
@country_controller.get('/cities/{city_id}', response={
    200: CityOut,
    404: MessageOut})
def get_city(request, city_id: UUID4):
    try:
        city = City.objects.get(id=city_id)
        return city
    except City.DoesNotExist:
        return 404, {'message': 'City not found.'}


@country_controller.get('/cites/{country_id}', response={
    200: CitySchema,
    404: MessageOut
})
def get_cities_by_country(request, country_id: UUID4, search=None, per_page: int = 12, page: int = 1):
    try:
        country = Country.objects.get(id=country_id)
        if search:
            cities = City.objects.filter(
                Q(city_name__icontains=search) and Q(country=country))
        else:
            cities = City.objects.filter(country=country)
        if cities:
            return response(status.HTTP_200_OK, cities, paginated=True, per_page=per_page, page=page)
        return 404, {'message': 'No cities found.'}
    except Country.DoesNotExist:
        return 404, {'message': 'Country not found.'}
