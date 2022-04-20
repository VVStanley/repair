from django.db import models


class Locomotive(models.Model):
    name = models.CharField(
        max_length=150,
        help_text='Название локомотива',
        unique=True
    )

    class Meta:
        verbose_name = 'Локомотив'
        verbose_name_plural = 'Локомотивы'

    def __str__(self):
        return self.name
