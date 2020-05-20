# Generated by Django 3.0.6 on 2020-05-20 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('salaries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Salary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=19)),
                ('taxes', models.DecimalField(decimal_places=2, max_digits=19)),
                ('received_at', models.DateTimeField(editable=False)),
            ],
        ),
    ]
