# Generated by Django 3.0.6 on 2020-05-21 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salaries', '0003_auto_20200520_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='taxes',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=19),
        ),
    ]
