from django import forms

from repairs.models import Repair


class RepairForm(forms.ModelForm):
    description = forms.CharField(
        label="Описание поломки",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )
    status = forms.CharField(
        label="Статус заявки",
        widget=forms.TextInput(
            attrs={'disabled': True, 'class': 'form-control'}
        )
    )
    time_to_work = forms.DateTimeField(
        label="Дата и время начало работы",
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control', 'type': 'datetime'}
        )
    )

    class Meta:
        model = Repair
        fields = ("description", "status", "time_to_work")
