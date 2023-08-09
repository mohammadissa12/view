from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
import datetime
from django.utils import timezone


from conf.utils.models import Entity

User = 'EmailAccount'


class EmailAccountManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = f'{self.model.USERNAME_FIELD}__iexact'
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, first_name, last_name, phone_number, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('user must have an phone_number to register')

        user = self.model(
            phone_number=phone_number
            , **extra_fields

        )
        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password):
        user = self.model(
            phone_number=phone_number
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    def create_admin(self, phone_number, password):
        user = self.model(
            phone_number=phone_number
        )
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_staff(self, phone_number, password):
        user = self.model(
            phone_number=phone_number
        )
        user.set_password(password)
        user.is_staff = True
        user.save(using=self._db)
        return user


class EmailAccount(AbstractUser, Entity):
    username = models.NOT_PROVIDED
    first_name = models.CharField('الاسم الاول', max_length=255)
    last_name = models.CharField('الاسم الثاني', max_length=255)
    email = models.EmailField('Email', blank=True, null=True)
    phone_number = models.IntegerField('رقم الهاتف', unique=True)
    image = models.ImageField('الصورة', upload_to='profile/', blank=True, null=True)

    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_merchant = models.BooleanField(default=False)
    merchant_expiry_date = models.DateField('تاريخ انتهاء العضوية', blank=True, null=True)
    is_free = models.BooleanField(default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = EmailAccountManager()

    class Meta:
        verbose_name = 'حساب'
        verbose_name_plural = 'حسابات'

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.phone_number}'

    def update_password(self, old_password, new_password):
        if self.check_password(old_password):
            self.set_password(new_password)
            self.save()
            return True
        return False

    def save(self, *args, **kwargs):
        if self.is_merchant and not self.merchant_expiry_date:
            self.merchant_expiry_date = timezone.now().date() + timezone.timedelta(days=365)
        elif self.merchant_expiry_date and timezone.now().date() > self.merchant_expiry_date:
            self.is_merchant = False

        super().save(*args, **kwargs)

    def is_merchant_expired(self):
        if  self.merchant_expiry_date:
            return timezone.date.today() > self.merchant_expiry_date
        return True

    @property
    def image_url(self):
        return (
            f"https://moamel.pythonanywhere.com{self.image.url}"
            if self.image
            else None
        )

    def has_perm(self, perm, obj=None):
        if self.is_superuser:
            return True

        # Give all permissions to is_admin except delete
        if self.is_admin and perm != 'delete':
            return True

        if self.is_staff and perm in ['account.EmailAccount', 'view_user', 'view_merchant', 'change_merchant',
                                      'view_profile', 'change_profile', ]:
            return True

        return super().has_perm(perm, obj)

    def has_module_perms(self, app_label):
        if self.is_superuser or self.is_admin:
            return True

        # Define your custom module-level permission checks for staff users
        if self.is_staff and app_label == 'account':
            return True

        return super().has_module_perms(app_label)


class AppDetails(Entity):
    app_version = models.CharField('رقم الاصدار التطبيق', max_length=100)

    def __str__(self):
        return self.app_version
