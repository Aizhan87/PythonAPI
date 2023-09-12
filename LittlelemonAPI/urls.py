from django.urls import path
from . import views

urlpatterns = [
    path('menu-items', views.menu_items),
    # path('menu-items', views.MenuItemsView.as_view()),
    path('menu-items/<int:id>', views.single_item),
    # path('category', views.CategoryItem.as_view()),
]