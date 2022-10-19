from ast import Delete
from urllib import response
from django.shortcuts import render
from .models import Post
from .serializers import PostSerializer
# from django.http import JsonResponse,HttpResponse
# from rest_framework.parsers import JSONParser
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# Class base views
from rest_framework.views import APIView
from django.http import Http404

from rest_framework import generics
from rest_framework import mixins

from rest_framework.authentication import SessionAuthentication, BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

genericView = generics.GenericAPIView
mixinList = mixins.ListModelMixin
mixinCreate = mixins.CreateModelMixin
mixinUpdate = mixins.UpdateModelMixin
mixinRetrieve = mixins.RetrieveModelMixin
mixinDestroy = mixins.DestroyModelMixin
genericViewSet = viewsets.GenericViewSet


class PostViewSet(genericViewSet,mixinList,mixinCreate,mixinDestroy,mixinRetrieve,mixinUpdate):
    serializer_class = PostSerializer
    queryset = Post.objects.all()





class genericAPIView(genericView, mixinList,mixinCreate,mixinUpdate,mixinRetrieve,mixinDestroy):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'
    authentication_classes = [SessionAuthentication,BasicAuthentication,TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self,request,id):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self,request):
        return self.create(request)

    def put(self,request,id=None):
        return self.update(request)

    def delete(self,request,id=None):
        return self.destroy(request)


class PostAPIView(APIView):
    def get(self,request):
        posts= Post.objects.all()
        serialzer = PostSerializer(posts, many=True)
        return Response(serialzer.data)

    def post(self,request):
        serialzer = PostSerializer(data=request.data)

        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data, status = status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)



class PostDetailAPIView(APIView):
    def get_object(self,id):
        try:
            return Post.objects.get(id=id)
        except Post.DoesNotExit:
            raise Http404

    def get(self,request,id):
        post = self.get_object(id)
        serializer=PostSerializer(post)
        return Response(serializer.data)

    def put(self,request,id):
        post = self.get_object(id)
        serializer = PostSerializer(post, request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,id):
        post = self.get_object(id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Create your views here.

@api_view(['GET','POST'])
def Posts(request):
    if request.method =='GET':
        posts= Post.objects.all()
        serialzer = PostSerializer(posts, many=True)
        return Response(serialzer.data)

    elif request.method == 'POST':
        serialzer = PostSerializer(data=request.data)

        if serialzer.is_valid():
            serialzer.save()
            return Response(serialzer.data, status = status.HTTP_201_CREATED)
        return Response(serialzer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','DELETE'])
def PostDetail(request,id):
    try:
        post = Post.objects.get(pk=id)
    except post.DoesNotExit:
        return response(status=404)

    if request.method == 'GET':
        serializer=PostSerializer(post)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = PostSerializer(post, request.data)
    
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        post.delete()
        return Response(status=204)