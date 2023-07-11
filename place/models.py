from datetime import date
from typing import List

from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver
from PIL import Image
from django.db import models
from location_field.models.plain import PlainLocationField
from django.contrib.contenttypes.models import ContentType

from conf.utils.models import Entity

User = get_user_model()


class PlaceMixin(Entity):
    PLACE_TYPE_CHOICES = [
        ('gas_station', 'محطة وقود'),
        ('entertainment', 'ترفيه'),
        ('gym', 'نادي رياضي'),
        ('restaurant', 'مطعم'),
        ('cafe', 'مقهى'),
        ('mall', 'مجمع تجاري'),

        ('stay_place', [
            ('hotel', 'فندق'),
            ('flat', 'شقق'),
            ('farm', 'مزرعة'),
        ]),

        ('health_centre',
         [
             ('hospital', 'مستشفى'),
             ('clinic', 'عيادة'),
             ('pharmacy', 'صيدلية'),
         ]),

        ('salon', [
            ('men_salon', 'صالون رجالي'),
            ('women_salon', 'صالون نسائي'),
        ]),
        ('tourist_place', [
            ('MUSEUM', 'متحف'),
            ('PARK', 'حديقة'),
            ('HISTORICAL_PLACE', 'مكان تاريخي'),
            ('waterfall', 'شلال'),
        ]),
        ('holy_place', [
            ('MOSQUE', 'مسجد'),
            ('CHURCH', 'كنيسة'),
            ('shrine', 'ضريح'),
        ]),
        ('financial_place', [
            ('BANK', 'بنك'),
            ('ATM', 'صراف آلي'),
            ('MONEY_EXCHANGE', 'صرافة'),
        ]),

    ]

    place_type = models.CharField('نوع المكان', max_length=50, choices=PLACE_TYPE_CHOICES)
    city = models.ForeignKey('location.City', on_delete=models.CASCADE)
    name = models.CharField('الاسم', max_length=50)
    description = models.TextField('الوصف', null=True, blank=True)
    place_details = models.TextField('تفاصيل المكان', null=True, blank=True)
    phone_number = models.CharField('رقم الهاتف', max_length=50, null=True, blank=True)
    short_location = models.CharField('الموقع', max_length=50, null=True, blank=True)
    location = PlainLocationField(based_fields=['city'], zoom=13, default='33.3152, 44.3661')

    def get_average_rating(self) -> float:
        return Reviews.objects.filter(place=self).aggregate(models.Avg('rating'))['rating__avg'] or 0

    def get_review_count(self) -> int:
        return Reviews.objects.filter(place=self).count()

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
    def place_social_media(self):
        return f'{self.social_media}'


class SocialMedia(Entity):
    place = models.OneToOneField(PlaceMixin, on_delete=models.CASCADE, related_name='social_media')
    facebook = models.URLField('فيسبوك', null=True, blank=True)
    instagram = models.URLField('انستجرام', null=True, blank=True)
    telegram = models.URLField('تليجرام', null=True, blank=True)
    whatsapp = models.URLField('واتساب', null=True, blank=True)
    is_available = models.BooleanField('متاح', default=True)

    class Meta:
        verbose_name = 'وسائل التواصل الاجتماعي'
        verbose_name_plural = 'وسائل التواصل الاجتماعي'


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
    rating = models.IntegerField('التقييم', default=0)

    def __str__(self):
        return f'{self.user} - {self.place}'

    class Meta:
        verbose_name = 'تعليق'
        verbose_name_plural = 'تعليقات'


class Advertisement(Entity):
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, verbose_name='الدولة', )
    place_type = models.CharField(max_length=50, choices=PlaceMixin.PLACE_TYPE_CHOICES, verbose_name='نوع المكان', )
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
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, verbose_name='الدولة', )
    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE, verbose_name='المكان')

    def __str__(self):
        return f'{self.place}'

    class Meta:
        verbose_name = 'مكان موصى به'
        verbose_name_plural = 'اماكن موصى بها'


class LatestPlaces(Entity):
    place = models.ForeignKey(PlaceMixin, on_delete=models.CASCADE, verbose_name='المكان')
    country = models.ForeignKey('location.Country', on_delete=models.CASCADE, verbose_name='الدولة', )

    def __str__(self):
        return f'{self.place}'

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
