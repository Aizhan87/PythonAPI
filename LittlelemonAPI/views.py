from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework import status 
from .models import MenuItem
from .models import Category 
from .serializers import MenuItemSerializer
from .serializers import CategorySerializer
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .throttles import TenCallsPerMinute
from django.contrib.auth.models import User, Group

@api_view(['GET', 'POST'])
# @throttle_classes([UserRateThrottle])
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

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({'message':'Some secret message'})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
         return Response({'message':'Only Manager should see this.'})
    else:
        return Response({'message':'You are not authorized'}, 403)

# johndoe token = "6954a798abee2dd79ea9355efb2d0b2a4aee8b33"
# jimmydoe token = "f25cd84dae39121d4b93e97f4594861ffb85eedd"

@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({'message': 'successful'})

@api_view()
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({'message': 'message for the logged in users only'})

@api_view(['POST', 'DELETE'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        if request.method == 'POST':
            managers.user_set.add(user)
        elif request.method == 'DELETE':
            managers.user_set.remove(user)
        return Response({'message': 'ok'})
    
    return Response({'message': 'error'}, status.HTTP_400_BAD_REQUEST)