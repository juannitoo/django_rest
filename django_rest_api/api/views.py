from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
 
from api.models import Category, Equipment
from api.serializers import CategoryListSerializer, CategoryDetailsSerializer
from api.serializers import EquipmentListSerializer, EquipmentDetailsSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100


class CategoryViewset(ModelViewSet):
    serializer_class = CategoryListSerializer
    details_serializer_class = CategoryDetailsSerializer
    pagination_class = StandardResultsSetPagination
    permission_classes = [IsAuthenticated]
    # filtres parent (simple)       
        # {
        #     "id": 14,
        #     "name": "Machines",
        #     "description": "tous types de machines"
        # },
        # {
        #     "id": 16,
        #     "name": "Engins",
        #     "description": "Machines de chantier"
        # },
        # {
        #     "id": 15,
        #     "name": "Outils",
        #     "description": "Outils portatifs manuels"
        # }
 
    def get_queryset(self):
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
        # get:retrieve get:list patch:partial_update  put:update  post:create  delete:destroy
        if self.action in ['retrieve', 'partial_update', 'update', 'create', 'destroy']:
            return self.details_serializer_class
        return super().get_serializer_class()

    def destroy(self, request, *args, **kwargs):
        categorie = self.get_object()
        if len(Equipment.objects.filter(categories=categorie)) == 0:
            categorie.delete()
            message = {'message': 'Catégory deleted'}
        else :
            message = {'message': 'Category can\'t be deleted, she\'s got childs'}
        return Response(message)


class EquipmentViewset(ModelViewSet):
    serializer_class = EquipmentListSerializer
    details_serializer_class = EquipmentDetailsSerializer
    pagination_class = StandardResultsSetPagination
    # permission_classes = [IsAuthenticated]
 
    def get_queryset(self):
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
        # get:retrieve get:list patch:partial_update  put:update  post:create destroy:delete get:list
        print(self.action)
        if self.action in ['retrieve', 'partial_update', 'update', 'create', 'destroy']:
            return self.details_serializer_class
        
        return super().get_serializer_class()
    