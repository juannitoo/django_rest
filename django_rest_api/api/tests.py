from django.test import TestCase
from authentication.models import User
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from api.models import Equipment, Category
from api.views import EquipmentViewset

# Note: force_authenticate directly sets request.user to the in-memory user instance. 
# If you are re-using the same user instance across multiple tests that update 
# the saved user state, you may need to call refresh_from_db() between tests.

from rest_framework.test import APITestCase
from api.models import Equipment, Category

class TestEquipment(APITestCase):

    # 'get': 'list',
    # 'post': 'create'
    # 'get': 'retrieve',
    # 'put': 'update',
    # 'patch': 'partial_update',
    # 'delete': 'destroy'

    def test_list_and_create(self):
        """
        Test GET and POST on list endpoint
        """
        category = Category.objects.create(
            name="Outils",
            slug="outils",
            description="outils portables"
        )
        equipement = Equipment.objects.create(
            name="Perceuse",
            slug="perceuse",
            description="perceuse description",
            quantity=5,
        )
        new_item = {
            "name":"Test",
            "slug":"test",
            "description":"Test description",
            "quantity":10,
            "categories": 1
        }

        factory = APIRequestFactory()
        user = User.objects.create(username="test", is_superuser=True, password="test")

        ## LIST
        view = EquipmentViewset.as_view({'get': 'list'})
        request = factory.get('/api/equipment/', format='json')
        force_authenticate(request, user=user, token=None)
        response = view(request)
        # status code ok
        self.assertEqual(response.status_code, 200)
        # give the good name
        self.assertEqual(response.data['results'][0]['name'],'Perceuse')
        # only 3 items, id name and description
        self.assertEqual(len(response.data['results'][0]), 3)

        ## POST
        view = EquipmentViewset.as_view({'post': 'create'})
        request = factory.post('/api/equipment/', new_item, format='json')
        force_authenticate(request, user=user, token=None)
        response = view(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['queryset'][0]['fields']['name'],'Test')
        # category is present
        self.assertEqual(response.data['queryset'][0]['fields']['categories'], [1])


    def test_update_and_partial_update(self):
        equipement = Equipment.objects.create(
            name="Perceuse",
            slug="perceuse",
            description="perceuse description",
            quantity=5,
        )
        category = Category.objects.create(
            name="Outils",
            slug="outils",
            description="outils portables"
        )
        new_item = {
            "name":"Meuleuse",
            "slug":"meuleuse",
            "description":"meuleuse description",
            "quantity":10,
            "categories":1,
        }

        factory = APIRequestFactory()
        user = User.objects.create(username="test", is_superuser=True, password="test")

        ## PUT
        view = EquipmentViewset.as_view({'put': 'update'})
        request = factory.put('/api/equipment/1/', new_item, format='json')
        force_authenticate(request, user=user, token=None)
        response = view(request, id=1) 
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['queryset'][0]['fields']['name'],'Meuleuse')

        ## PATCH
        view = EquipmentViewset.as_view({'patch': 'partial_update'})
        request = factory.patch('/api/equipment/1/', {"name" : "Betonnière"} , format='json')
        force_authenticate(request, user=user, token=None)
        response = view(request, id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'],'Betonnière')


    def test_retrieve_and_destroy(self):
        equipement = Equipment.objects.create(
            name="Perceuse",
            slug="perceuse",
            description="perceuse description",
            quantity=5,
        )

        factory = APIRequestFactory()
        user = User.objects.create(username="test", is_superuser=True, password="test")

        view = EquipmentViewset.as_view({'get': 'retrieve'})
        request = factory.get('/api/equipment/1/', format='json')
        force_authenticate(request, user=user, token=None)
        response = view(request, id=1)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'],'Perceuse')
        # 6 items, id name description quantity slug categories
        self.assertEqual(len(response.data), 6)

        view = EquipmentViewset.as_view({'delete': 'destroy'})
        request = factory.delete('/api/equipment/1/', format='json')
        force_authenticate(request, user=user, token=None)
        response = view(request, id=1)
        # status 204 deletion ok
        self.assertEqual(response.status_code, 204)
