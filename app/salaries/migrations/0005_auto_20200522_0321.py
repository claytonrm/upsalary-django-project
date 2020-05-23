# Generated by Django 3.0.6 on 2020-05-22 03:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payees', '0001_initial'),
        ('salaries', '0004_auto_20200521_0619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='salary',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='payees.Payee'),
        ),
        migrations.DeleteModel(
            name='Payee',
        ),
    ]