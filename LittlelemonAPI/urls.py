from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items', views.menu_items),
    path('menu-items/<int:id>', views.single_item),
    path('category/<int:pk>',views.category_detail, name='category-detail'),
    path('secret/', views.secret),
    path('api-token-auth/', obtain_auth_token),
    path('manager-view/', views.manager_view),
    path('throttle-check/', views.throttle_check),
    path('throttle-check-auth/', views.throttle_check_auth),
    path('groups/manager/users', views.managers),
]


# http://127.0.0.1:8000/apis/secret
# http://127.0.0.1:8000/apis/groups/manager/users