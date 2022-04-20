from django import forms

from repairs.models import Repair, TypesRepair, PlacesWork
from repairs.models.repair import statuses_technician


class TechnicianForm(forms.ModelForm):
    """Форма для техника"""
    description = forms.CharField(
        label="Описание поломки",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    time_to_work = forms.DateTimeField(
        label="Дата и время начало работы",
        widget=forms.DateTimeInput(attrs={'class': 'form-control'}),
    )
    places_to_work = forms.ModelChoiceField(
        label='Место для ремонта',
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=PlacesWork.objects.all()
    )
    type_repair = forms.ModelChoiceField(
        label='Тип ремонта',
        widget=forms.Select(attrs={'class': 'form-control'}),
        queryset=TypesRepair.objects.all()
    )
    status = forms.ChoiceField(
        label='Установите статус заявки',
        choices=statuses_technician,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = Repair
        fields = (
            "description", "time_to_work",
            "places_to_work", "type_repair", "status"
        )
