from django.db import models
from django.db.models import Avg, Sum

from conf.utils.models import Entity
from place.models import PlaceMixin


class Country(Entity):
    class CountryChoices(models.TextChoices):
        IRAQ = 'IRAQ', 'العراق'
        TURKEY = 'TURKEY', 'تركيا'
        EGYPT = 'EGYPT', 'مصر'
        SAUDI_ARABIA = 'SAUDI_ARABIA', 'السعودية'
        UNITED_ARAB_EMIRATES = 'UNITED_ARAB_EMIRATES', 'الامارات العربية المتحدة'
        SYRIA = 'SYRIA', 'سورية'
        LEBANON = 'LEBANON', 'لبنان'
        IRAN = 'IRAN', 'ايران'
        TUNISIA = 'TUNISIA', 'تونس'
        OMAN = 'OMAN', 'عمان'
        MALAYSIA = 'MALAYSIA', 'ماليزيا'
        BALI = 'BALI', 'بالي'
        GEORGIA = 'GEORGIA', 'جورجيا'
        AZERBAIJAN = 'AZERBAIJAN', 'اذربيجان'

    country_name = models.CharField('اسم الدولة', max_length=50, unique=True, choices=CountryChoices.choices,
                                    default=CountryChoices.IRAQ)

    def __str__(self):
        return f'{self.country_name}'

    class Meta:
        verbose_name = 'الدولة'
        verbose_name_plural = 'الدول'

    @property
    def get_cities(self):
        return self.country_city.all()

    @property
    def get_advertisements(self):
        return self.advertisements.all()

    @property
    def get_recommended_places(self):
        return self.recommended_places.all()

    @property
    def get_latest_places(self):
        return self.latest_places.all()

    @property
    def get_offers(self):
        return self.offers.all()

    @property
    def get_company(self):
        return self.company.all()

class City(Entity):
    city_name = models.CharField('اسم المدينة', max_length=50, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='country_city')

    def __str__(self):
        return f'{self.city_name}-{self.country.country_name}'

    class Meta:
        verbose_name = 'المدينة'
        verbose_name_plural = 'المدن'

    @property
    def get_advertisements(self):
        return self.advertisements.all()

    @property
    def get_latest_places(self):
        return self.latest_places.all()

    @property
    def get_high_rated(self):
        return self.city_places.all().order_by('-reviews__rating')[:5]
