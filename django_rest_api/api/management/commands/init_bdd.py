from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from api.models import *

UserModel = get_user_model()

CATEGORIES = [
    {
        'name': 'Outils',
        'description' : "Outils portatifs manuels",
        'slug': 'outils-portatifs',
        'parent': '',
        'Equipment': [
            {
                'name': 'Perceuse',
                'description' : "Perceuse à percussion Hilti 2500w",
                'quantity' : 20,
                'slug': 'perceuse-percussion',
                'categories': ['Outils'],
            },
            {
                'name': 'Perceuse sans fil',
                'description' : "Perceuse sans fil Hilti 1000w",
                'quantity' : 20,
                'slug': 'perceuse-percussion',
                'categories': ['Outils'],
            },
            {
                'name': 'Visseuse',
                'description' : "Visseuse sans fil Hilti 1000w",
                'quantity' : 15,
                'slug': 'visseuse-sans-fil',
                'categories': ['Outils'],
            },
            {
                'name': 'Meuleuse',
                'description' : "Meuleuse Hilti 1500w",
                'quantity' : 5,
                'slug': 'meuleuse',
                'categories': ['Outils'],
            },
        ]
    },
    {
        'name': 'Engins',
        'description' : "Machines de chantier",
        'slug': 'machine-de-chantier',
        'parent':'',
        'Equipment': [
            {
                'name': 'Tractopelle',
                'description' : "Mini tractopelle JCB 3DX",
                'quantity' : 1,
                'slug': 'petit-tractopelle',
                'categories': ['Engins'],
            },
            {
                'name': 'Betonnière',
                'description' : "betonnière electrique Hilti",
                'quantity' : 5,
                'slug': 'betonniere-electrique',
                'categories': ['Engins'],
            },
            {
                'name': 'Marteau-piqueur',
                'description' : "Marteau-Piqueur Hilti",
                'quantity' : 2,
                'slug': 'marteau-piqueur',
                'categories': ['Engins', 'Outils'],
            },
        ]
    },
]

ADMIN_ID = 'admin'
ADMIN_PASSWORD = 'nautilux'
ADMIN_MAIL = 'xx@hxx.fr'

class Command(BaseCommand):

    help = 'Initialisation de la base de données en local'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING(self.help))

        Category.objects.all().delete()
        Equipment.objects.all().delete()

        machine = Category.objects.create(
            name="Machines",
            description="tous types de machines",
            slug="machines",
        )

        for cat in CATEGORIES:
            Category.objects.create(
                name=cat['name'],
                description=cat['description'],
                slug=cat['slug'],
                parent=machine,
            )
            for c in cat['Equipment'] :    
                equipement = Equipment.objects.create(
                    name=c['name'],
                    description=c['description'],
                    quantity=c['quantity'],
                    slug=c['slug'],
                )
                equipement.categories.set(Category.objects.filter(name__in=[x for x in c['categories']]))
                equipement.save()


        UserModel.objects.create_superuser(ADMIN_ID, ADMIN_MAIL, ADMIN_PASSWORD)

        self.stdout.write(self.style.SUCCESS("All Done !"))

