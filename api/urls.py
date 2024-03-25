# urls.py
from django.urls import path
from api.views import LoginView, LogoutView, InventoryView, UserView
from rest_framework.authtoken import views

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('inventory/', InventoryView.as_view()),
    path('users/', UserView.as_view()),
]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
