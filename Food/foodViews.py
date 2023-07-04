from django.http import JsonResponse
from .models import Food
from .foodSerializers import FoodSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.core.cache import cache
from django.contrib.auth.decorators import login_required, user_passes_test
from .foodPrivateMethods import __get_food, __create_food

#without dependency injection
@api_view(['GET', 'POST'])
#@login_required
def food_list(request):
    if request.method == 'GET':
        food_data = __get_food()
        return JsonResponse({'Food': food_data})

    if request.method == 'POST':
        data = request.data
        created_food_data = __create_food(data)
        if not isinstance(created_food_data, dict):
            return JsonResponse(created_food_data, status=400)
        return JsonResponse(created_food_data, status=201)


def is_admin(user):
    return user.groups.filter(name='admin').exists()


#dependency injection and cache
@swagger_auto_schema(
    method='get',
    operation_id='food_list',
    responses={
        status.HTTP_200_OK: openapi.Response(description='Get food list.'),
    }
)

@api_view(['GET'])
@login_required
def foodList(request, food_model=Food, food_serializer=FoodSerializer):
    if request.method == 'GET':
        cache_key = 'food_list_cache'
        cached_data = cache.get(cache_key)
        if cached_data:
            print('Retrieved data from cache:', cached_data)
            return Response(cached_data)

        food = food_model.objects.all()
        serializer = food_serializer(food, many=True)
        data = {'Food': serializer.data}

        # Cache the data for future requests
        cache.set(cache_key, data, 60 * 5)  # Cache for 5 minutes (300 seconds)
        print('Stored data in cache:', data)

        return Response(data)


@swagger_auto_schema(
    method='post',
    operation_id='food_create',
    request_body=FoodSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response(description='Food created.'),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description='Invalid request.'),
    }
)

@api_view(['POST'])
@user_passes_test(is_admin)
@login_required
def foodCreate(request, food_serializer=FoodSerializer):
    if request.method == 'POST':
        serializer = food_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_id='food_read',
    responses={
        status.HTTP_200_OK: openapi.Response(description='Food read.'),
    }
)

@api_view(['GET'])
@login_required
def foodRead(id, food_model=Food, food_serializer=FoodSerializer):
    try:
        food = food_model.objects.get(pk=id)
    except food_model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = food_serializer(food)
    return Response(serializer.data)


@swagger_auto_schema(
    method='put',
    operation_id='food_update',
    request_body=FoodSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(description='Food updated.'),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description='Invalid request.'),
    }
)

@api_view(['PUT'])
@user_passes_test(is_admin)
@login_required
def foodUpdate(request, id, food_model=Food, food_serializer=FoodSerializer):
    try:
        food = food_model.objects.get(pk=id)
    except food_model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = food_serializer(food, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='delete',
    operation_id='food_delete',
    responses={
        status.HTTP_204_NO_CONTENT: openapi.Response(description='Food deleted.'),
        status.HTTP_404_NOT_FOUND: openapi.Response(description='Food not found.'),
    }
)

@api_view(['DELETE'])
@user_passes_test(is_admin)
@login_required
def foodDelete(id, food_model=Food):
    try:
        food = food_model.objects.get(pk=id)
    except food_model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    food.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
