# Generated by Django 4.2.3 on 2023-07-27 04:08

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0001_initial'),
        ('place', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('Company_name', models.CharField(max_length=50, verbose_name='اسم الشركة')),
                ('image', models.ImageField(upload_to='company', verbose_name='الصورة')),
                ('short_description', models.CharField(max_length=100, verbose_name='الوصف المختصر')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='location.country', verbose_name='الدولة')),
            ],
            options={
                'verbose_name': 'شركة',
                'verbose_name_plural': 'الشركات',
            },
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(upload_to='offers', verbose_name='الصورة')),
                ('title', models.CharField(max_length=50, verbose_name='العنوان')),
                ('short_description', models.CharField(max_length=100, verbose_name='الوصف المختصر')),
                ('url', models.URLField(blank=True, max_length=100, null=True, verbose_name='الرابط')),
                ('start_date', models.DateField(verbose_name='تاريخ البداية')),
                ('end_date', models.DateField(verbose_name='تاريخ النهاية')),
                ('is_active', models.BooleanField(default=False, verbose_name='مفعل')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='location.country', verbose_name='الدولة')),
                ('place', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='offers', to='place.placemixin', verbose_name='المكان')),
            ],
            options={
                'verbose_name': 'عرض',
                'verbose_name_plural': 'العروض',
            },
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('trip_name', models.CharField(max_length=50, verbose_name='اسم الرحلة')),
                ('image', models.ImageField(upload_to='trip', verbose_name='الصورة')),
                ('short_description', models.CharField(max_length=100, verbose_name='الوصف المختصر')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trip', to='place.company', verbose_name='الشركة')),
            ],
            options={
                'verbose_name': 'رحلة',
                'verbose_name_plural': 'الرحلات',
            },
        ),
        migrations.CreateModel(
            name='TripDetails',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('trip_name', models.CharField(max_length=50, verbose_name='اسم الرحلة')),
                ('trip', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='trip_details', to='place.trip', verbose_name='الرحلة')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Offer',
        ),
    ]
