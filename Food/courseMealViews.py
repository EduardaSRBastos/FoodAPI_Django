from .models import CourseMealCategory
from .courseMealSerializers import CourseMealSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.decorators import login_required
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.views.decorators.cache import cache_page

#cache
@swagger_auto_schema(
    method='get',
    operation_id='courseMeal_list',
    responses={
        status.HTTP_200_OK: openapi.Response(description='Get course meals list.'),
    }
)

@cache_page(60 * 5)  # Cache for 5 minutes (300 seconds)
@api_view(['GET'])
@login_required
def courseMealList(request, course_meal_model=CourseMealCategory, course_meal_serializer=CourseMealSerializer):
    if request.method == 'GET':
        courseMeal = course_meal_model.objects.all()
        serializer = course_meal_serializer(courseMeal, many=True)
        return Response({'Course Meal': serializer.data})


@swagger_auto_schema(
    method='post',
    operation_id='courseMeal_create',
    request_body=CourseMealSerializer,
    responses={
        status.HTTP_201_CREATED: openapi.Response(description='Course Meal created.'),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description='Invalid request.'),
    }
)

@api_view(['POST'])
@login_required
def courseMealCreate(request, course_meal_serializer=CourseMealSerializer):
    if request.method == 'POST':
        serializer = course_meal_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='get',
    operation_id='courseMeal_read',
    responses={
        status.HTTP_200_OK: openapi.Response(description='Course Meal read.'),
    }
)

@api_view(['GET'])
@login_required
def courseMealRead(id, course_meal_model=CourseMealCategory, course_meal_serializer=CourseMealSerializer):
    try:
        courseMeal = course_meal_model.objects.get(pk=id)
    except course_meal_model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = course_meal_serializer(courseMeal)
    return Response(serializer.data)


@swagger_auto_schema(
    method='put',
    operation_id='courseMeal_update',
    request_body=CourseMealSerializer,
    responses={
        status.HTTP_200_OK: openapi.Response(description='Course Meal updated.'),
        status.HTTP_400_BAD_REQUEST: openapi.Response(description='Invalid request.'),
    }
)

@api_view(['PUT'])
@login_required
def courseMealUpdate(request, id, course_meal_model=CourseMealCategory, course_meal_serializer=CourseMealSerializer):
    try:
        courseMeal = course_meal_model.objects.get(pk=id)
    except course_meal_model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    serializer = course_meal_serializer(courseMeal, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='delete',
    operation_id='courseMeal_delete',
    responses={
        status.HTTP_204_NO_CONTENT: openapi.Response(description='Course Meal deleted.'),
        status.HTTP_404_NOT_FOUND: openapi.Response(description='Course Meal not found.'),
    }
)

@api_view(['DELETE'])
@login_required
def courseMealDelete(id, course_meal_model=CourseMealCategory):
    try:
        courseMeal = course_meal_model.objects.get(pk=id)
    except course_meal_model.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    courseMeal.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
