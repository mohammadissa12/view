from datetime import date
from django.contrib.auth import get_user_model
from math import radians, cos, sin, asin, sqrt

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import F
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from PIL import Image
from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from account.models import EmailAccount
from conf.utils.models import Entity

User = get_user_model()


class PlaceType(Entity):
    class PlaceTypeChoices(models.TextChoices):
        restaurant = 'restaurant', 'مطعم'
        stayplace = 'stayplace', 'مكان اقامة'
        cafe = 'cafe', 'مقهى'
        touristplace = 'touristplace', 'مكان سياحي'
        mall = 'mall', 'مول'
        healthcenter = 'healthcenter', 'مركز صحي'
        holyplace = 'holyplace', 'مكان مقدس'
        financial = 'financial', 'مالي'
        gasstation = 'gasstation', 'محطة وقود'
        entertainment = 'entertainment', 'ترفيهي'
        sport = 'sport', 'رياضي'
        salons = 'salons', 'صالونات'

    name = models.CharField('الاسم', max_length=50, choices=PlaceTypeChoices.choices, )

    def __str__(self):
        return self.name


class PlaceSubType(Entity):
    name = models.CharField('الاسم', max_length=50, )
    place_type = models.ForeignKey(PlaceType, on_delete=models.CASCADE, related_name='place_type_sub_types', )

    def __str__(self):
        return f'{self.name} - {self.place_type}'


class PlaceMixin(Entity):
    user = models.ForeignKey(EmailAccount, on_delete=models.CASCADE, related_name='user_places', null=True, blank=True)
    place_type = models.ForeignKey(PlaceType, on_delete=models.CASCADE, related_name='places', )
    type = models.ForeignKey(PlaceSubType, on_delete=models.CASCADE, related_name='place_sub_type_places', null=True,
                             blank=True)
    city = models.ForeignKey('location.City', on_delete=models.CASCADE, related_name='city_places')
    name = models.CharField('الاسم', max_length=50, )
    description = models.TextField('الوصف', )
    phone_number = models.CharField('رقم الهاتف', max_length=50, null=True, blank=True)
    short_location = models.CharField('الموقع', max_length=50, )
    location = PlainLocationField(based_fields=['city'], zoom=13, default='33.3152, 44.3661')
    price = models.FloatField('السعر', max_length=50, null=True, blank=True)
    open = models.CharField('المتاح', max_length=50, null=True, blank=True)

    is_archived = models.BooleanField('تم الأرشفة', default=False)

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
        return f'{self.name} - {self.city} '

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

    @property
    def get_place_type(self):
        try:
            return self.place_type.name
        except PlaceType.DoesNotExist:
            return None

    @property
    def get_place_sub_type(self):
        return self.type.name if self.type else None

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #
    #     if self.user.is_merchant_expired():
    #         print("Merchant is expired. Archiving the place.")
    #         # Merchant is expired, archive the place
    #         self.is_archived = True
    #         self.save(update_fields=['is_archived'])
    #     else:
    #         print("Merchant is not expired. Place remains active.")


class SocialMedia(Entity):
    place = models.OneToOneField(PlaceMixin, on_delete=models.CASCADE, related_name='social_media', null=True,
                                 blank=True)
    facebook = models.CharField('فيسبوك', null=True, blank=True, max_length=50)
    instagram = models.CharField('انستغرام', null=True, blank=True, max_length=50)
    telegram = models.CharField('تليجرام', null=True, blank=True, max_length=50)
    whatsapp = models.CharField('واتساب', null=True, blank=True, max_length=50)

    class Meta:
        verbose_name = 'وسائل التواصل الاجتماعي'
        verbose_name_plural = 'وسائل التواصل الاجتماعي'

    SOCIAL_MEDIA_APPS = {
        'facebook': 'facebook',
        'instagram': 'instagram',
        'telegram': 'telegram',
        'whatsapp': 'whatsapp',
    }

    @property
    def is_available(self):
        available_apps = []
        if self.facebook:
            available_apps.append(self.SOCIAL_MEDIA_APPS['facebook'])
        if self.instagram:
            available_apps.append(self.SOCIAL_MEDIA_APPS['instagram'])
        if self.telegram:
            available_apps.append(self.SOCIAL_MEDIA_APPS['telegram'])
        if self.whatsapp:
            available_apps.append(self.SOCIAL_MEDIA_APPS['whatsapp'])
        return available_apps


class Images(Entity):
    image = models.ImageField('الصورة', upload_to='images/')
    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE, related_name='images')

    def __str__(self):
        return f'{self.image}'

    @property
    def image_url(self):
        domain = "https://moamel.pythonanywhere.com"  # Replace this with your actual domain
        return f"{domain}{self.image.url}"

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
    comment = models.TextField('التعليق', null=True, blank=True,)
    rating = models.PositiveSmallIntegerField('التقييم', default=1,
                                              validators=[MinValueValidator(1), MaxValueValidator(5)])
    reported = models.BooleanField('تم الابلاغ', default=False)  # New field for reporting

    def __str__(self):
        return f'{self.user} - {self.place}'

    class Meta:
        verbose_name = 'تعليق'
        verbose_name_plural = 'تعليقات'



class Advertisement(Entity):
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, verbose_name='الدولة',
                                related_name='advertisements', null=True, blank=True)
    city = models.ForeignKey('location.City', on_delete=models.CASCADE, verbose_name='المدينة',
                             related_name='advertisements', blank=True, null=True)

    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE, verbose_name='المكان',
                              related_name='advertisements', blank=True, null=True)
    image = models.ImageField('الصورة', upload_to='advertisements')
    title = models.CharField('العنوان', max_length=50)
    short_description = models.CharField('الوصف المختصر', max_length=100)
    url = models.URLField('الرابط', max_length=100, blank=True, null=True)
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


class Offers(Entity):
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, verbose_name='الدولة',
                                related_name='offers')
    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE, verbose_name='المكان', related_name='offers',
                              blank=True, null=True)
    image = models.ImageField('الصورة', upload_to='offers')
    url = models.URLField('الرابط', max_length=100, blank=True, null=True)
    start_date = models.DateField('تاريخ البداية')
    end_date = models.DateField('تاريخ النهاية', )
    is_active = models.BooleanField('مفعل', default=False)

    def __str__(self):
        return f'{self.title} '

    class Meta:
        verbose_name = 'عرض'
        verbose_name_plural = 'العروض'


@receiver(pre_save, sender=Offers)
def set_active(sender, instance, **kwargs):
    if instance.end_date < date.today():
        instance.is_active = False


class RecommendedPlaces(Entity):
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, verbose_name='الدولة',
                                related_name='recommended_places')
    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE, verbose_name='المكان')

    def __str__(self):
        return f'{self.place}'

    class Meta:
        verbose_name = 'مكان موصى به'
        verbose_name_plural = 'اماكن موصى بها'


class LatestPlaces(Entity):
    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE, verbose_name='المكان')
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, verbose_name='الدولة',
                                related_name='latest_places')
    city = models.ForeignKey('location.City', on_delete=models.CASCADE, verbose_name='المدينة',
                             related_name='latest_places', null=True, blank=True)

    def __str__(self):
        return f'{self.place.name}'

    class Meta:
        verbose_name = 'احدث الاماكن'
        verbose_name_plural = 'احدث الاماكن'


@receiver(post_save)
def latest_place_handler(sender, instance, created, **kwargs):
    if issubclass(sender, PlaceMixin) and created:
        country = instance.city.country if instance.city else None
        LatestPlaces.objects.create(place=instance, country=country, city=instance.city)


class FavoritePlaces(Entity):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_places')
    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE, verbose_name='المكان',
                              related_name='favorite_places')

    def __str__(self):
        return f'{self.user} - {self.place}'

    class Meta:
        verbose_name = 'مكان مفضل'
        verbose_name_plural = 'اماكن مفضلة'


class Company(Entity):
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, verbose_name='الدولة',
                                related_name='company')
    city = models.ForeignKey('location.City', on_delete=models.CASCADE, verbose_name='المدينة', related_name='company',
                             blank=True, null=True)
    company_name = models.CharField('اسم الشركة', max_length=50)
    image = models.ImageField('الصورة', upload_to='company')
    company_description = models.CharField('وصف الشركة', max_length=100)

    def __str__(self):
        return f'{self.country.country_name}{self.company_name}'

    class Meta:
        verbose_name = 'شركة'
        verbose_name_plural = 'الشركات'

    @classmethod
    def get_companies_by_city_name(cls, city_name):
        return cls.objects.filter(city__city_name=city_name)



class Trip(Entity):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='الشركة', related_name='trip')
    trip_name = models.CharField('اسم الرحلة', max_length=50)
    short_description = models.CharField('الوصف المختصر', max_length=100)

    def __str__(self):
        return f'{self.company.company_name}{self.trip_name}'

    class Meta:
        verbose_name = 'رحلة'
        verbose_name_plural = 'الرحلات'

    @property
    def company_description(self):
        return self.company.company_description


class TripDetails(Entity):
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, verbose_name='الرحلة', related_name='trip_details')
    trip_name = models.CharField('اسم الرحلة', max_length=50)
    trip_details = models.TextField('تفاصيل الرحلة', max_length=256)
    location = PlainLocationField(based_fields=['city'], zoom=13, default='33.3152, 44.3661',
                                  verbose_name='موقع الشركة')

    def __str__(self):
        return f'{self.trip_name}'

    class Meta:
        verbose_name = 'تفاصيل الرحلة'
        verbose_name_plural = 'تفاصيل الرحلات'

    @property
    def lat(self):
        return self.location.latitude

    @property
    def lng(self):
        return self.location.longitude

    @property
    def trip_images(self):
        return self.trip_image.all()

    @property
    def social_media(self):
        try:
            return self.trip_social_media
        except TripSocialMedia.DoesNotExist:
            return None


class TripImages(Entity):
    trip = models.ForeignKey(TripDetails, on_delete=models.CASCADE, verbose_name='الرحلة', related_name='trip_image')
    image = models.ImageField('الصورة', upload_to='trip_images')

    def __str__(self):
        return f'{self.trip.trip_name}'

    class Meta:
        verbose_name = 'صورة الرحلة'
        verbose_name_plural = 'صور الرحلات'

    @property
    def trip_image_url(self):
        domain = "https://moamel.pythonanywhere.com"  # Replace this with your actual domain
        return f"{domain}{self.image.url}"

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 500 or img.width > 500:
            output_size = (500, 500)
            img.thumbnail(output_size)
            img.save(self.image.path)


class TripSocialMedia(Entity):
    trip = models.ForeignKey(TripDetails, on_delete=models.CASCADE, verbose_name='الرحلة',
                             related_name='trip_social_media', null=True, blank=True)
    facebook = models.CharField('فيسبوك', null=True, blank=True, max_length=50)
    instagram = models.CharField('انستغرام', null=True, blank=True, max_length=50)
    telegram = models.CharField('تليجرام', null=True, blank=True, max_length=50)
    whatsapp = models.CharField('واتساب', null=True, blank=True, max_length=50)

    def __str__(self):
        return f'{self.trip.trip_name}'

    class Meta:
        verbose_name = 'وسائل التواصل الاجتماعي'
        verbose_name_plural = 'وسائل التواصل الاجتماعي'

    SOCIAL_MEDIA_APPS = {
        'facebook': 'facebook',
        'instagram': 'instagram',
        'telegram': 'telegram',
        'whatsapp': 'whatsapp',
    }

    @property
    def is_available(self):
        available_apps = []
        if self.facebook:
            available_apps.append(self.SOCIAL_MEDIA_APPS['facebook'])
        if self.instagram:
            available_apps.append(self.SOCIAL_MEDIA_APPS['instagram'])
        if self.telegram:
            available_apps.append(self.SOCIAL_MEDIA_APPS['telegram'])
        if self.whatsapp:
            available_apps.append(self.SOCIAL_MEDIA_APPS['whatsapp'])
        return available_apps
