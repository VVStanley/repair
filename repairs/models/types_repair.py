from django.db import models


class TypesRepair(models.Model):
    name = models.CharField(
        max_length=250,
        help_text='Тип ремонта',
        unique=True
    )
    houers = models.PositiveSmallIntegerField(
        help_text='количество часов ремонта'
    )

    class Meta:
        verbose_name = 'Тип ремонта'
        verbose_name_plural = 'Типы ремонта'

    def __str__(self):
        return self.name
