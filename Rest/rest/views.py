
from django.http import JsonResponse,Http404
from .models import Drink
from .serializer import DrinkSerializer

#importing api views 
from rest_framework.decorators import api_view

#import response from rest_framework also give us  nice interface to see our data
from rest_framework.response import Response
# import status to get server state
from rest_framework import status


@api_view(['GET','POST'])
def drinkList(request,format=None):

    if request.method == 'GET':
        #get all the drinks from DB
        get_list = Drink.objects.all()

        #serialize the drinks
        serialize_list = DrinkSerializer(get_list, many=True)

        #return json format
        return Response({'drinks': serialize_list.data})
    
    if request.method == 'POST':
        #assign the request data to a serializer to create a new data
        serializer_object = DrinkSerializer(data = request.data)

        #check if the data exit
        if serializer_object.is_valid():
            serializer_object.save()
            
            #return reponse to the client
            return Response(serializer_object.data, status=status.HTTP_201_CREATED)


@api_view(['GET','PUT','DELETE'])
def drinkDetail(request,id,format=None):
    #get the object from Model
    try:
        drink_object = Drink.objects.get(id=id)
    except drink_object.DoesNotExit:
        #Return not found if the page does not exit
        raise Response(status = status.HTTP_404_NOT_FOUND) 

    if  request.method == 'GET':
        #serialize the drink object
        serialize_object = DrinkSerializer(drink_object)
        #return  reponse
        return Response(serialize_object.data)

    elif request.method == 'PUT':
        serialize_object = DrinkSerializer(drink_object, data=request.data)
        if serialize_object.is_valid():
            serialize_object.save()
            return Response(serialize_object.data)
        return Response(serialize_object.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        drink_object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    

    
    
