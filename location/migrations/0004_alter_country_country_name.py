# Generated by Django 4.2.3 on 2023-07-21 04:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0003_alter_country_country_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='country',
            name='country_name',
            field=models.CharField(choices=[('IRAQ', 'العراق'), ('TURKEY', 'تركيا'), ('EGYPT', 'مصر'), ('SAUDI_ARABIA', 'السعودية'), ('UNITED_ARAB_EMIRATES', 'الامارات العربية المتحدة'), ('SYRIA', 'سورية'), ('LEBANON', 'لبنان'), ('IRAN', 'ايران'), ('TUNISIA', 'تونس'), ('OMAN', 'عمان'), ('MALAYSIA', 'ماليزيا'), ('BALI', 'بالي'), ('GEORGIA', 'جورجيا'), ('AZERBAIJAN', 'اذربيجان')], default='IRAQ', max_length=50, unique=True, verbose_name='اسم الدولة'),
        ),
    ]
