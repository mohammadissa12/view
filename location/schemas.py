from typing import List

from ninja import Schema
from pydantic import UUID4


class CountryOut(Schema):
    id: UUID4
    country_name: str


class CountrySchema(Schema):
    total_count: int = None
    per_page: int = None
    from_record: int = None
    to_record: int = None
    previous_page: int = None
    next_page: int = None
    current_page: int = None
    page_count: int = None
    data: List[CountryOut]


class CityOut(Schema):
    id: UUID4
    city_name: str
    country: CountryOut


class CitySchema(Schema):
    total_count: int = None
    per_page: int = None
    from_record: int = None
    to_record: int = None
    previous_page: int = None
    next_page: int = None
    current_page: int = None
    page_count: int = None
    data: List[CityOut]


class City2(Schema):
    id: UUID4
    city_name: str
