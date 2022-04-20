from django.db import models


class PlacesWork(models.Model):
    """Места для ремонта"""
    name = models.CharField(
        max_length=100,
        help_text='Ввелите название места для ремонта',
        unique=True
    )

    class Meta:
        verbose_name = 'Место ремонта'
        verbose_name_plural = 'Места ремонта'

    def __str__(self):
        return self.name
