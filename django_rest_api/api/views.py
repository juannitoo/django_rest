from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
 
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
    # filtres parent (simple)       
    # [('Machines', UUID('344ea79e-2936-4d47-8d13-2ffa4f92a447')), 
    #  ('Engins', UUID('cdd8723a-9924-403d-b9df-a8b1fddf096f')), 
    #  ('Outils', UUID('a7febc7d-b598-46bc-850d-07bfac8fbee2')), 
    #  ('test3', UUID('2a76edb3-e755-4f8f-bccc-3d5faa4abf86'))]>
 
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
        # get:retireve patch:partial_update  put:update  post:create  delete:destroy
        if self.action in ['retrieve', 'partial_update', 'update', 'create', 'destroy']:
            return self.details_serializer_class
           
        return super().get_serializer_class()
    

class EquipmentViewset(ModelViewSet):
    serializer_class = EquipmentListSerializer
    details_serializer_class = EquipmentDetailsSerializer
    pagination_class = StandardResultsSetPagination
 
    def get_queryset(self):
        queryset = Equipment.objects.all()
        filters = {}

        # [('Machines', UUID('344ea79e-2936-4d47-8d13-2ffa4f92a447')), 
        #  ('Engins', UUID('cdd8723a-9924-403d-b9df-a8b1fddf096f')), 
        #  ('Outils', UUID('a7febc7d-b598-46bc-850d-07bfac8fbee2')), 
        #  ('test', UUID('67807648-a11f-482e-9aa2-5fcadb0b61c5'))]>

        try :
        # categories je ne sais pas trop, depuis postman j'envoie ca :
        # categories : 96ea9ab4-4468-454a-a4d8-a0e9a18f4367orfe99f3fd-74c3-40db-9094-19c1030fba7e
        # ca fonctionne
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
        # get:retireve patch:partial_update  put:update  post:create destroy:delete
        print(self.action)
        if self.action in ['retrieve', 'partial_update', 'update', 'create', 'destroy']:
            return self.details_serializer_class
        
        return super().get_serializer_class()
    