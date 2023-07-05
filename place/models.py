from PIL.Image import Image
from django.db import models
from location_field.models.plain import PlainLocationField

from conf.utils.models import Entity


class Images(Entity):
    image = models.ImageField('الصورة', upload_to='images/')
    place = models.ForeignKey('PlaceMixin', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.image}'

    class Meta:
        verbose_name = 'صورة'
        verbose_name_plural = 'صور'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        super().save(*args, **kwargs)

        # img = Image.open(self.image.path)
        # if img.height > 500 or img.width > 500:
        #     output_size = (500, 500)
        #     img.thumbnail(output_size)
        #     img.save(self.image.path)


class Reviews(Entity):
    user = models.ForeignKey('account.ProfileUser', on_delete=models.CASCADE)
    place = models.ForeignKey('PlaceMixin', on_delete=models.CASCADE)
    comment = models.TextField('التعليق', null=True, blank=True)
    rating = models.IntegerField('التقييم', default=0)

    def __str__(self):
        return f'{self.user} - {self.place}'

    class Meta:
        verbose_name = 'تعليق'
        verbose_name_plural = 'تعليقات'


class PlaceMixin(Entity):
    city = models.ForeignKey('location.City', on_delete=models.CASCADE)
    name = models.CharField('الاسم', max_length=50)
    description = models.TextField('الوصف', null=True, blank=True)
    location = PlainLocationField(based_fields=['city'], zoom=13, default='33.3152, 44.3661')

    def average_rating(self) -> float:
        return Reviews.objects.filter(place=self).aggregate(models.Avg('rating'))['rating__avg'] or 0

    @property
    def latitude(self):
        return float(self.location.split(',')[0])

    @property
    def longitude(self):
        return float(self.location.split(',')[1])

    def __str__(self):
        return f'{self.name} - {self.city} - {self.latitude} - {self.longitude}'

    @property
    def images(self):
        return self.images.all()


class Restaurant(PlaceMixin):
    class Meta:
        verbose_name = 'مطعم'
        verbose_name_plural = 'مطاعم'


class StayPlace(PlaceMixin):
    class StayPlaceType(models.TextChoices):
        Hotel = 'فندق', 'فندق'
        Resort = 'منتجع', 'منتجع'
        Motel = 'موتيل', 'موتيل'
        Hostel = 'نزل', 'نزل'
        chalet = 'شاليه', 'شاليه'

    type = models.CharField('نوع', choices=StayPlaceType.choices, max_length=50, default=StayPlaceType.Hotel)

    class Meta:
        verbose_name = 'مكان اقامة'
        verbose_name_plural = 'اماكن اقامة'


class Cafeteria(PlaceMixin):
    class Meta:
        verbose_name = 'كافيه'
        verbose_name_plural = 'كافيهات'


class TouristPlace(PlaceMixin):
    CHOICES = (
        (
            ('اماكن سياحية', (
                ('مصيف', 'مصيف'),
                ('متحف', 'متحف'),
                ('شلال', 'شلال'),
            )),
            ('اماكن عامة', (
                ('منتزه', 'منتزه'),
                ('متحف', 'متحف'),
                ('معلم حضاري', 'معلم حضاري'),
            )),
        ))

    type = models.CharField('نوع المكان', choices=CHOICES, max_length=50, )

    class Meta:
        verbose_name = 'مكان سياحي'
        verbose_name_plural = 'أماكن سياحية'


class Mall(PlaceMixin):
    class Meta:
        verbose_name = 'مول'
        verbose_name_plural = 'مولات'


class HealthCentre(PlaceMixin):
    class HealthCentreType(models.TextChoices):
        Hospital = 'مستشفى', 'مستشفى'
        Clinic = 'عيادة', 'عيادة'
        Pharmacy = 'صيدلية', 'صيدلية'

    type = models.CharField('نوع المركز', choices=HealthCentreType.choices, max_length=50, )

    class Meta:
        verbose_name = 'مركز صحي'
        verbose_name_plural = 'مراكز صحية'


class HolyPlace(PlaceMixin):
    class HolyPlaceType(models.TextChoices):
        Mosque = 'مسجد', 'مسجد'
        Church = 'كنيسة', 'كنيسة'
        Shrine = 'ضريح', 'ضريح'

    type = models.CharField('نوع المكان', choices=HolyPlaceType.choices, max_length=50, )

    class Meta:
        verbose_name = 'مكان مقدس'
        verbose_name_plural = 'أماكن مقدسة'


class Financial(PlaceMixin):
    class FinancialType(models.TextChoices):
        Bank = 'بنك', 'بنك'
        ATM = 'Atm', 'ATM'
        Exchange = 'صرافة', 'صرافة'

    type = models.CharField('نوع المكان', choices=FinancialType.choices, max_length=50, )

    class Meta:
        verbose_name = 'الخدمة المالية'
        verbose_name_plural = 'الخدمات المالية'


class GasStation(PlaceMixin):
    class Meta:
        verbose_name = 'محطة وقود'
        verbose_name_plural = 'محطات وقود'


class Entertainment(PlaceMixin):
    class Meta:
        verbose_name = ' مكان ترفيهي'
        verbose_name_plural = 'اماكن ترفيهية'


class Gym(PlaceMixin):
    class Meta:
        verbose_name = 'مكان رياضي'
        verbose_name_plural = 'اماكن رياضية'


class Salons(PlaceMixin):
    class SalonType(models.TextChoices):
        barber = 'حلاق رجالي', 'حلاق رجالي'
        salon = 'صالون نسائي', 'صالون نسائي'

    type = models.CharField('نوع المكان', choices=SalonType.choices, max_length=50, )

    class Meta:
        verbose_name = 'حلاقة وصالون'
        verbose_name_plural = 'حلاقة وصالونات'
