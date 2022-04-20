from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Status(models.TextChoices):
    RAW = 'CREATED', 'Новая заявка от клиента'  # Видит техник
    CONFIRMED = 'CONFIRMED', 'Подтверждена техником'  # Видит мастер
    READY_TO_WORK = 'READY_TO_WORK', 'Готова к работе'  # Видит слесарь
    PROGRESS = 'PROGRESS', 'В работе'  # Слесарь взял в работу
    VERIFICATION = 'VERIFICATION', 'Ремонт выполнен'  # Слесарь сдал на тест
    TESTS = 'TESTS', 'На тестировании'  # На испытаниях у мастера
    RE_REPAIR = 'RE_REPAIR', 'На доработку'  # Мастер вернул на доработку


statuses_technician = [
    item for item in Status.choices if item[0] == 'CONFIRMED'
]
statuses_master = [
    item for item in Status.choices if item[0] in (
        'READY_TO_WORK', 'TESTS', 'RE_REPAIR'
    )
]
statuses_worker = [
    item for item in Status.choices if item[0] in (
         'PROGRESS', 'VERIFICATION'
    )
]


class Repair(models.Model):
    users = models.ManyToManyField(
        to='users.User',
        related_name='repairs',
        verbose_name='Участники заявки'
    )
    description = models.TextField(
        help_text='Описание поломки'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        verbose_name='Статус заявки'
    )
    time_to_work = models.DateTimeField(
        verbose_name="Дата и время начало работы",
        null=True, blank=True
    )
    places_to_work = models.ForeignKey(
        'repairs.PlacesWork',
        verbose_name='Место для ремонта',
        on_delete=models.PROTECT,
        related_name='place_repairs',
        null=True, blank=True
    )
    locomotove = models.ForeignKey(
        'repairs.Locomotive',
        verbose_name='Локомотив',
        on_delete=models.PROTECT,
        related_name='locomotive_repairs',
        null=True, blank=True
    )
    type_repair = models.ForeignKey(
        'repairs.TypesRepair',
        verbose_name='Тип ремонта',
        on_delete=models.PROTECT,
        related_name='type_repairs',
        null=True, blank=True
    )
    works = models.ManyToManyField(
        to='repairs.Work',
        verbose_name='Работы',
        related_name='work_repairs'
    )
    parts = models.ManyToManyField(
        to='repairs.Parts',
        verbose_name='Запчасти',
        related_name='part_repairs'
    )

    class Meta:
        verbose_name = 'Заявка на ремонт'
        verbose_name_plural = 'Заявки на ремонт'

    def __str__(self):
        return 'repair'

    def get_absolute_url(self):
        """Ссылка на детальную запись"""
        return reverse(f'repairs:detail', kwargs={'repair_id': self.id})
