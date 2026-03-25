from django.urls import path
from . import views

urlpatterns = [
    # Основные маршруты для записей
    path('', views.transaction_list, name='transaction_list'),
    path('create/', views.transaction_create, name='transaction_create'),
    path('<int:pk>/edit/', views.transaction_edit, name='transaction_edit'),
    path('<int:pk>/delete/', views.transaction_delete, name='transaction_delete'),
    
    # Управление справочниками
    path('directories/<str:model_name>/', views.directory_list, name='directory_list'),
    path('directories/<str:model_name>/create/', views.directory_create, name='directory_create'),
    path('directories/<str:model_name>/<int:pk>/edit/', views.directory_edit, name='directory_edit'),
    path('directories/<str:model_name>/<int:pk>/delete/', views.directory_delete, name='directory_delete'),
    
    # API для динамической загрузки
    path('api/categories/', views.api_categories, name='api_categories'),
    path('api/subcategories/', views.api_subcategories, name='api_subcategories')
]