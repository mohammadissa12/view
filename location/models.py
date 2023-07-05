from django.db import models
from conf.utils.models import Entity


class Country(Entity):
    country_name = models.CharField('اسم الدولة', max_length=50, unique=True)

    def __str__(self):
        return f'{self.country_name}'

    class Meta:
        verbose_name = 'الدولة'
        verbose_name_plural = 'الدول'


class City(Entity):
    city_name = models.CharField('اسم المدينة', max_length=50, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.city_name}-{self.country.country_name}'

    class Meta:
        verbose_name = 'المدينة'
        verbose_name_plural = 'المدن'
