from rest_framework import serializers
from .models import MenuItem
from .models import Category
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']
        
        
class MenuItemSerializer(serializers.ModelSerializer):
    price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','stock', 'price_after_tax','category','category_id']
        extra_kwargs = {
            'price': {'min_value': 2},
            'stock':{'source':'inventory', 'min_value': 0}
        }

    def calculate_tax(self, product:MenuItem):
        return product.price * Decimal(1.1)
    
    
# Create a HyperLinkedRelatedField in the serializer

# class MenuItemSerializer(serializers.ModelSerializer):
#     stock = serializers.IntegerField(source='inventory')
#     price_after_tax = serializers.SerializerMethodField(method_name = 'calculate_tax')
#     category = serializers.HyperlinkedRelatedField(
#         queryset = Category.objects.all(),
#         view_name='category-detail'
#     )
#     class Meta:
#         model = MenuItem
#         fields = ['id','title','price','stock', 'price_after_tax','category']       
#     def calculate_tax(self, product:MenuItem):
#         return product.price * Decimal(1.1)