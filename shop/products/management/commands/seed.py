from django.core.management.base import BaseCommand
from ...models import Category


class Command(BaseCommand):
    help = "Створює початкові категорії для маркетплейсу"

    def handle(self, *args, **kwargs):
        categories = [
            {"name": "Електроніка", "description": "Всі види електроніки"},
            {"name": "Одяг", "description": "Чоловічий та жіночий одяг"},
            {"name": "Книги", "description": "Книги та література"},
        ]

        for cat in categories:
            Category.objects.get_or_create(
                name=cat["name"],
                defaults={"description": cat["description"]}
            )

        self.stdout.write(self.style.SUCCESS("Категорії успішно створено!"))
