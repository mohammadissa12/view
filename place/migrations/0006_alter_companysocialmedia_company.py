# Generated by Django 4.2.3 on 2023-08-26 17:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0005_remove_tripdetails_location_company_location_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companysocialmedia',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_social_media', to='place.company', verbose_name='الشركة '),
        ),
    ]
