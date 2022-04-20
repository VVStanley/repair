from django import forms
from django.contrib.auth import get_user_model

from repairs.models import Repair, Parts
from repairs.models.repair import statuses_master
from users.models import Role

User = get_user_model()


class MasterForm(forms.ModelForm):
    """Форма для мастера"""
    parts = forms.ModelMultipleChoiceField(
        label="Запчасти",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        queryset=Parts.objects.all()
    )
    users = forms.ModelChoiceField(
        label="Назначте слесаря",
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=User.objects.filter(role=Role.WORKER)
    )
    status = forms.ChoiceField(
        label='Установите статус заявки',
        choices=statuses_master,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Repair
        fields = ("parts", "users", "status")
