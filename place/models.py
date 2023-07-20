from datetime import date
from typing import List

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericRelation
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image
from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.contenttypes.models import ContentType

from conf.utils.models import Entity

User = get_user_model()


class PlaceMixin(Entity):
    city = models.ForeignKey('location.City', on_delete=models.CASCADE,related_name='city_places')
    name = models.CharField('الاسم', max_length=50,)
    description = models.TextField('الوصف', )
    phone_number = models.CharField('رقم الهاتف', max_length=50, null=True, blank=True)
    short_location = models.CharField('الموقع', max_length=50, )
    location = PlainLocationField(based_fields=['city'], zoom=13, default='33.3152, 44.3661')

    def get_average_rating(self) -> float:
        return Reviews.objects.filter(place=self).aggregate(models.Avg('rating'))['rating__avg'] or 0

    def get_review_count(self) -> int:
        return Reviews.objects.filter(place=self).count()

    @property
    def average_rating(self):
        return self.get_average_rating()

    @property
    def review_count(self):
        return self.get_review_count()

    @property
    def latitude(self):
        return float(self.location.split(',')[0])

    @property
    def longitude(self):
        return float(self.location.split(',')[1])

    def __str__(self):
        return f'{self.name} - {self.city} - {self.latitude} - {self.longitude}'

    @property
    def place_images(self):
        return self.images.all()

    @property
    def reviews(self):
        return self.reviews.all()

    @property
    def get_social_media(self):
        try:
            return self.social_media
        except SocialMedia.DoesNotExist:
            return None

class SocialMedia(Entity):
    place = models.OneToOneField(PlaceMixin, on_delete=models.CASCADE, related_name='social_media', null=True, blank=True)
    facebook = models.CharField('فيسبوك', null=True, blank=True, max_length=50)
    instagram = models.CharField('انستغرام', null=True, blank=True, max_length=50)
    telegram = models.CharField('تليجرام', null=True, blank=True, max_length=50)
    whatsapp = models.CharField('واتساب', null=True, blank=True, max_length=50)


    class Meta:
        verbose_name = 'وسائل التواصل الاجتماعي'
        verbose_name_plural = 'وسائل التواصل الاجتماعي'

    @property
    def social_media_links(self):
        links = {}
        if self.facebook:
            links['facebook'] = self.facebook
        if self.instagram:
            links['instagram'] = self.instagram
        if self.telegram:
            links['telegram'] = self.telegram
        if self.whatsapp:
            links['whatsapp'] = self.whatsapp
        return links


class Images(Entity):
    image = models.ImageField('الصورة', upload_to='images/')
    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.image}'

    class Meta:
        verbose_name = 'صورة'
        verbose_name_plural = 'صور'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)


class Reviews(Entity):
    user = models.ForeignKey('account.EmailAccount', on_delete=models.CASCADE)
    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE)
    comment = models.TextField('التعليق', null=True, blank=True)
    rating = models.PositiveSmallIntegerField('التقييم', default=1,
                                              validators=[MinValueValidator(1), MaxValueValidator(5)])
    reported = models.BooleanField('تم الابلاغ', default=False)  # New field for reporting

    def __str__(self):
        return f'{self.user} - {self.place}'

    class Meta:
        verbose_name = 'تعليق'
        verbose_name_plural = 'تعليقات'


class Restaurant(PlaceMixin):
    advertisement = GenericRelation('Advertisement', related_query_name='restaurant')

    class Meta:
        verbose_name = 'مطعم'
        verbose_name_plural = 'مطاعم'



class StayPlace(PlaceMixin):
    class StayPlaceType(models.TextChoices):
        Hotel = 'فندق', 'فندق'
        flat = 'شقق', 'شقق'
        farm = 'مزرعة', 'مزرعة'

    advertisement = GenericRelation('Advertisement', related_query_name='stay_place')
    type = models.CharField('نوع', choices=StayPlaceType.choices, max_length=50, default=StayPlaceType.Hotel)

    class Meta:
        verbose_name = 'مكان اقامة'
        verbose_name_plural = 'اماكن اقامة'


class Cafe(PlaceMixin):
    advertisement = GenericRelation('Advertisement', related_query_name='cafeteria')

    class Meta:
        verbose_name = 'كافيه'
        verbose_name_plural = 'كافيهات'


class TouristPlace(PlaceMixin):
    CHOICES = (
        (
            ('tourist_place  ', (
                ('مصيف', 'مصيف'),
                ('متحف', 'متحف'),
                ('شلال', 'شلال'),
                ('منتزه', 'منتزه'),
                ('متحف', 'متحف'),
                ('معلم حضاري', 'معلم حضاري'),
            )),
        ))

    advertisement = GenericRelation('Advertisement', related_query_name='tourist_place')
    type = models.CharField('نوع المكان', choices=CHOICES, max_length=50, )

    class Meta:
        verbose_name = 'مكان سياحي'
        verbose_name_plural = 'أماكن سياحية'


class Mall(PlaceMixin):
    advertisement = GenericRelation('Advertisement', related_query_name='mall')

    class Meta:
        verbose_name = 'مول'
        verbose_name_plural = 'مولات'


class HealthCentre(PlaceMixin):
    class HealthCentreType(models.TextChoices):
        Hospital = 'مستشفى', 'مستشفى'
        Clinic = 'عيادة', 'عيادة'
        Pharmacy = 'صيدلية', 'صيدلية'

    advertisement = GenericRelation('Advertisement', related_query_name='health_centre')
    type = models.CharField('نوع المركز', choices=HealthCentreType.choices, max_length=50, )

    class Meta:
        verbose_name = 'مركز صحي'
        verbose_name_plural = 'مراكز صحية'


class HolyPlace(PlaceMixin):
    class HolyPlaceType(models.TextChoices):
        Mosque = 'مسجد', 'مسجد'
        Church = 'كنيسة', 'كنيسة'
        Shrine = 'ضريح', 'ضريح'

    advertisement = GenericRelation('Advertisement', related_query_name='holy_place')
    type = models.CharField('نوع المكان', choices=HolyPlaceType.choices, max_length=50, )

    class Meta:
        verbose_name = 'مكان مقدس'
        verbose_name_plural = 'أماكن مقدسة'


class Financial(PlaceMixin):
    class FinancialType(models.TextChoices):
        Bank = 'بنك', 'بنك'
        ATM = 'Atm', 'ATM'
        Exchange = 'صرافة', 'صرافة'

    advertisement = GenericRelation('Advertisement', related_query_name='financial')
    type = models.CharField('نوع المكان', choices=FinancialType.choices, max_length=50, )

    class Meta:
        verbose_name = 'الخدمة المالية'
        verbose_name_plural = 'الخدمات المالية'


class GasStation(PlaceMixin):
    advertisement = GenericRelation('Advertisement', related_query_name='gas_station')

    class Meta:
        verbose_name = 'محطة وقود'
        verbose_name_plural = 'محطات وقود'


class Entertainment(PlaceMixin):
    advertisement = GenericRelation('Advertisement', related_query_name='entertainment')

    class Meta:
        verbose_name = ' مكان ترفيهي'
        verbose_name_plural = 'اماكن ترفيهية'


class Gym(PlaceMixin):
    advertisement = GenericRelation('Advertisement', related_query_name='gym')

    class Meta:
        verbose_name = 'مكان رياضي'
        verbose_name_plural = 'اماكن رياضية'


class Salons(PlaceMixin):
    class SalonType(models.TextChoices):
        barber = 'حلاق رجالي', 'حلاق رجالي'
        salon = 'صالون نسائي', 'صالون نسائي'

    advertisement = GenericRelation('Advertisement', related_query_name='salons')
    type = models.CharField('نوع المكان', choices=SalonType.choices, max_length=50, )

    class Meta:
        verbose_name = 'حلاقة وصالون'
        verbose_name_plural = 'حلاقة وصالونات'


class Advertisement(Entity):
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, verbose_name='الدولة',related_name='advertisements' )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name='نوع المكان', null=True,
                                     blank=True)
    image = models.ImageField('الصورة', upload_to='advertisements')
    title = models.CharField('العنوان', max_length=50)
    short_description = models.CharField('الوصف المختصر', max_length=100)
    url = models.URLField('الرابط', max_length=100, blank=True, null=True)
    place = models.ForeignKey('PlaceMixin', on_delete=models.CASCADE, verbose_name='المكان', null=True, blank=True)
    start_date = models.DateField('تاريخ البداية')
    end_date = models.DateField('تاريخ النهاية', )
    is_active = models.BooleanField('مفعل', default=False)

    def __str__(self):
        return f'{self.title} '

    class Meta:
        verbose_name = 'اعلان'
        verbose_name_plural = 'الاعلانات'


@receiver(pre_save, sender=Advertisement)
def set_active(sender, instance, **kwargs):
    if instance.end_date < date.today():
        instance.is_active = False


class RecommendedPlaces(Entity):
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, verbose_name='الدولة',related_name='recommended_places' )
    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE, verbose_name='المكان')

    def __str__(self):
        return f'{self.place}'

    class Meta:
        verbose_name = 'مكان موصى به'
        verbose_name_plural = 'اماكن موصى بها'


class LatestPlaces(Entity):
    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE, verbose_name='المكان')
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, verbose_name='الدولة',related_name='latest_places' )

    def __str__(self):
        return f'{self.place.name}'

    class Meta:
        verbose_name = 'احدث الاماكن'
        verbose_name_plural = 'احدث الاماكن'


class FavoritePlaces(Entity):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_places')
    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE, verbose_name='المكان',
                              related_name='favorite_places')

    def __str__(self):
        return f'{self.user} - {self.place}'

    class Meta:
        verbose_name = 'مكان مفضل'
        verbose_name_plural = 'اماكن مفضلة'
