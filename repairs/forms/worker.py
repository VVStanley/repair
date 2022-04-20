from django import forms

from repairs.models import Repair
from repairs.models.repair import statuses_worker


class WorkerForm(forms.ModelForm):
    """Форма для слесаря"""
    status = forms.ChoiceField(
        label='Установите статус заявки',
        choices=statuses_worker,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Repair
        fields = ("status",)
