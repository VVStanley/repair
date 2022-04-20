from django.db import models


class Work(models.Model):
    name = models.CharField(
        max_length=200,
        help_text='Работа',
        unique=True
    )
    type_repair = models.ForeignKey(
        'repairs.TypesRepair',
        on_delete=models.PROTECT,
        related_name="works"
    )

    class Meta:
        verbose_name = 'Работа'
        verbose_name_plural = 'Работы'

    def __str__(self):
        return self.name
