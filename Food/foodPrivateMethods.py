from .models import Food
from .foodSerializers import FoodSerializer

def __get_food():
    food = Food.objects.all()
    serializer = FoodSerializer(food, many=True)
    return serializer.data

def __create_food(data):
    serializer = FoodSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return serializer.errors