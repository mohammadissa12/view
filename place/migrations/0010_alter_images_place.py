# Generated by Django 4.2.1 on 2023-07-06 23:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0009_socialmedia_placemixin_phone_number_delete_contact_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='images',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='place.placemixin'),
        ),
    ]
