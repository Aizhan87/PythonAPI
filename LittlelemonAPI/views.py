from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status 
from .models import MenuItem
from .models import Category 
from .serializers import MenuItemSerializer
from .serializers import CategorySerializer
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage

@api_view(['GET', 'POST'])
def menu_items(request):
    if request.method == 'GET':
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        perpage = request.query_params.get('perpage', default=2)
        page = request.query_params.get('page', default=1)
        if category_name: 
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price__lte=to_price)
            # http://127.0.0.1:8000/apis/menu-items?to_price=7.50&category=Dessert
        if search:
            items = items.filter(title__icontains=search)
            # http://127.0.0.1:8000/apis/menu-items?search=Chocolate
        if ordering:
            # items = items.order_by(ordering) -> order by 1 item
            # http://127.0.0.1:8000/apis/menu-items?ordering=price  -> ascending order
            # http://127.0.0.1:8000/apis/menu-items?ordering=-price -> descending order
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
            # http://127.0.0.1:8000/apis/menu-items?ordering=title,price
        
        paginator = Paginator(items,per_page=perpage)
        try:
            items = paginator.page(number=page)
            # http://127.0.0.1:8000/apis/menu-items?perpage=3&page=2
        except EmptyPage:
            items = []
        serialized_item = MenuItemSerializer(items, many=True, context={'request': request})
        return Response(serialized_item.data)
    if request.method == 'POST':
        serialized_item = MenuItemSerializer(data=request.data)
        serialized_item.is_valid(raise_exception=True)
        serialized_item.save()
        return Response(serialized_item.data, status.HTTP_201_CREATED)
    
# limit = request.GET.get(‘limit’)
# MenuItem.objects.raw('SELECT * FROM LittleLemonAPI_menuitem LIMIT %s', [limit]) 

@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serialized_item = MenuItemSerializer(item)
    return Response(serialized_item.data)

@api_view()
def category_detail(request, pk):
    category = get_object_or_404(Category,pk=pk)
    serialized_category = CategorySerializer(category)
    return Response(serialized_category.data) 