# Generated by Django 4.0.4 on 2022-04-19 14:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('repairs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='repair',
            name='users',
            field=models.ManyToManyField(related_name='repairs', to=settings.AUTH_USER_MODEL, verbose_name='Участники заявки'),
        ),
        migrations.AddField(
            model_name='repair',
            name='works',
            field=models.ManyToManyField(related_name='work_repairs', to='repairs.work', verbose_name='Работы'),
        ),
    ]
