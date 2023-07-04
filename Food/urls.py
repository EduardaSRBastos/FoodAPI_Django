"""
URL configuration for Food project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from Food import foodViews as food_views
from Food import courseMealViews as course_meal_views
from Food.Accounts.accountsViews import register, user_login, user_logout
from rest_framework.urlpatterns import format_suffix_patterns
from .swagger import schema_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', food_views.foodList),
    path('food/list/', food_views.food_list),
    path('food/', food_views.foodList, name='food_list'),
    path('food/create/', food_views.foodCreate, name='food_create'),
    path('food/<int:id>/', food_views.foodRead, name='food_read'),
    path('food/<int:id>/update/', food_views.foodUpdate, name='food_update'),
    path('food/<int:id>/delete/', food_views.foodDelete, name='food_delete'),
    path('courseMeals/', course_meal_views.courseMealList, name='course_meal_list'),
    path('courseMeals/create/', course_meal_views.courseMealCreate, name='course_meal_create'),
    path('courseMeals/<int:id>/', course_meal_views.courseMealRead, name='course_meal_read'),
    path('courseMeals/<int:id>/update/', course_meal_views.courseMealUpdate, name='course_meal_update'),
    path('courseMeals/<int:id>/delete/', course_meal_views.courseMealDelete, name='course_meal_delete'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

#urlpatterns = format_suffix_patterns(urlpatterns)

