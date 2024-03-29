from django.core.serializers import serialize
import json
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
 
from api.models import Category, Equipment
from api.serializers import CategoryListSerializer, CategoryDetailsSerializer
from api.serializers import EquipmentListSerializer, EquipmentDetailsSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """
    Pagination's parameters
    """
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryViewset(ModelViewSet):
    """
    Retrieve and use category's data
    """
    serializer_class = CategoryListSerializer
    details_serializer_class = CategoryDetailsSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
 

    def get_queryset(self):
        """
        Category CRUD endpoints and url filters
        """
        queryset = Category.objects.all()
        filters = {}
        try :
            parent = self.request.GET.get('parent')
            if parent is not None:
                filters['parent'] = Category.objects.get(id=parent)
        except Exception as e :
            print(f'fail category queryset filters : {e}')
        return queryset.filter(**filters).distinct()
    

    def get_serializer_class(self):
        """
        Decide which serailizer is used
        """
        # get:retrieve get:list patch:partial_update  put:update  post:create  delete:destroy
        if self.action in ['retrieve', 'partial_update', 'update', 'create', 'destroy']:
            return self.details_serializer_class
        return super().get_serializer_class()


    def destroy(self, request, *args, **kwargs):
        """
        Override the delete method to lock it if category has child
        """
        categorie = self.get_object()
        message = {}
        if len(Equipment.objects.filter(categories=categorie)) == 0:
            categorie.delete()
            message = {'message': 'Catégory deleted'}
        else :
            message = {'message': 'Category can\'t be deleted, she\'s got childs'}
        return Response(message)




class EquipmentViewset(ModelViewSet):
    """
    Retrieve and use equipment's data
    """
    serializer_class = EquipmentListSerializer
    details_serializer_class = EquipmentDetailsSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "id"
 

    def get_queryset(self):
        """
        Equipment CRUD endpoints and url filters
        """
        queryset = Equipment.objects.all()
        filters = {}
        try :
            # categories je ne sais pas trop, depuis postman j'envoie ca :
            # categories : 1or2 et ca fonctionne
            cat = self.request.GET.get('categories')
            if cat is not None:
                if 'or' in cat :
                    cat_list = cat.split('or')
                    filters['categories__id__in'] = cat_list
                else :
                    filters['categories__id'] = cat

            quantity_min = self.request.GET.get('quantity_min')
            quantity_max = self.request.GET.get('quantity_max')
            if quantity_min is not None and quantity_max is not None :
                filters['quantity__lte'] = int(quantity_max)
                filters['quantity__gte'] = int(quantity_min)
            elif quantity_min is not None and quantity_max is None: 
                filters['quantity__gte'] = int(quantity_min)
            elif quantity_max is not None and quantity_min is None:
                filters['quantity__lte'] = int(quantity_max)
                
        except Exception as e :
            print(f'fail equipment queryset filters : {e}')

        return queryset.filter(**filters).distinct()
    

    def get_serializer_class(self):
        """
        Decide which serializer is used
        """
        if self.action in ['retrieve', 'partial_update', 'update', 'create', 'destroy']:
            return self.details_serializer_class   
        return super().get_serializer_class()
    

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            equipment = Equipment.objects.create(
                name=data['name'],
                slug=data['slug'],
                description=data['description'],
                quantity=data['quantity'],
            )
            equipment.categories.add(data['categories'])
            equipment.save()
            serialized_data = serialize("json", Equipment.objects.filter(id=equipment.id))
            serialized_data = json.loads(serialized_data)
            return Response({'queryset': serialized_data}, status=201)
        except Exception as e:
            print("exception create:", e)
            return Response({'queryset': "fail"}, status=400)


    def update(self, request, *args, **kwargs):
        try : 
            id = self.kwargs.get(self.lookup_url_kwarg)
            data = request.data
            equipment = Equipment.objects.get(id=id)
            equipment.name=data['name']
            equipment.slug=data['slug']
            equipment.description=data['description']
            equipment.quantity=data['quantity']
            cat = data['categories']
            if Category.objects.get(id=cat) not in [ x for x in equipment.categories.all() ]:
                equipment.categories.add(Category.objects.get(id=cat))
                equipment.save()
            else : 
                equipment.categories.remove(Category.objects.get(id=cat))
                equipment.save()
            serialized_data = serialize("json", Equipment.objects.filter(id=id))
            serialized_data = json.loads(serialized_data)
            return Response({'queryset': serialized_data}, status=200)
        except Exception as e:
            print("exception update:", e)
            return Response({'queryset': "fail"}, status=400)


    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
