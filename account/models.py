from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


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
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class EmailAccount(AbstractUser):
    id = models.AutoField(primary_key=True)
    username = models.NOT_PROVIDED
    first_name = models.CharField('الاسم الاول', max_length=255)
    last_name = models.CharField('الاسم الثاني', max_length=255)
    email = models.EmailField('Email', blank=True, null=True)
    phone_number = models.IntegerField('رقم الهاتف', unique=True)
    is_verified = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = EmailAccountManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.phone_number}'

    def update_password(self, old_password, new_password):
        if self.check_password(old_password):
            self.set_password(new_password)
            self.save()
            return True
        return False

    class Meta:
        verbose_name = 'حساب'
        verbose_name_plural = 'حسابات'


class ProfileUser(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(EmailAccount, on_delete=models.CASCADE)
    image = models.ImageField('الصورة', upload_to='profile/', blank=True, null=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} {self.user.phone_number}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f'{self.user.first_name} {self.user.last_name}'

    @property
    def phone_number(self):
        return self.user.phone_number

    class Meta:
        verbose_name = 'الملف الشخصي '
        verbose_name_plural = 'الملفات الشخصية'


@receiver(post_save, sender=EmailAccount)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        ProfileUser.objects.create(user=instance)





