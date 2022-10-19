from dataclasses import field
from rest_framework import serializers
from .models import Post


# class PostSerializer(serializers.Serializer):
#     title = serializers.CharField(max_length=200)
#     autor = serializers.CharField(max_length=150)
#     email = serializers.EmailField(default='')


#     def create(self,validate_data):
#         return Post.objects.create(validate_data)

#     def update(self, instance, validated_data):
#         instance.title = validated_data.get('title',validated_data.title)
#         instance.author = validated_data.get('author',validated_data.author)
#         instance.email = validated_data.get('email',validated_data.email)




class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title','autor','email']