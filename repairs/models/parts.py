from django.db import models


class Parts(models.Model):
    name = models.CharField(
        max_length=150,
        help_text='Название запчасти',
        unique=True
    )

    class Meta:
        verbose_name = 'Запчасть'
        verbose_name_plural = 'Запчасти'

    def __str__(self):
        return self.name
