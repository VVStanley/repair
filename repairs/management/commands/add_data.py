from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from repairs.management.commands.data import (
    locomotives_data,
    places_work_data,
    types_repair_data,
    parts_data,
    users_data,
)
from repairs.models import Locomotive, PlacesWork, Parts, TypesRepair, Work

User = get_user_model()


class Command(BaseCommand):
    help = 'fill DB data'

    def handle(self, *args, **options):
        for locomotive in locomotives_data:
            Locomotive.objects.get_or_create(name=locomotive)

        for place_work in places_work_data:
            PlacesWork.objects.get_or_create(name=place_work)

        for part in parts_data:
            Parts.objects.get_or_create(name=part)

        for user_data in users_data:
            User.objects.get_or_create(
                first_name=user_data[0],
                last_name=user_data[1],
                username=user_data[2],
                email=user_data[3],
                role=user_data[4],
                password=make_password(user_data[5])
            )

        for type_repair in types_repair_data:
            new_type_repair, _ = TypesRepair.objects.get_or_create(
                name=type_repair['name'], houers=type_repair['houers']
            )
            for work in type_repair['work']:
                Work.objects.get_or_create(
                    name=work, type_repair=new_type_repair
                )
