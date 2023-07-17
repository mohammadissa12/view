# Generated by Django 4.2.3 on 2023-07-15 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('place', '0003_alter_placemixin_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='socialmedia',
            name='place',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='social_media', to='place.placemixin'),
        ),
    ]
