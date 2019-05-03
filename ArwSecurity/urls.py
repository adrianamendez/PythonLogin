# accounts/urls.py
from django.urls import path, include
from rest_framework import routers
from ArwSecurity import views

router = routers.DefaultRouter()
router.register(r'product', views.ProductsViewSet)
#router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('api-token-auth/', views.CustomAuthToken.as_view(), name='api_token_auth'),
    path('users/', views.user_list),

]
