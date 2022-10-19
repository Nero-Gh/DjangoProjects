from django.urls import path,include
from .views import PostAPIView,PostDetailAPIView, PostViewSet,genericAPIView
from rest_framework import routers


router = routers.SimpleRouter()
router.register('posts',PostViewSet,basename='posts')
urlpatterns = [
    # path('posts/',Posts),
    # path('details/<int:id>',PostDetail)
    # path('posts/', PostAPIView.as_view()),
    # path('postdetail/<int:id>', PostDetailAPIView.as_view())

    # path('GenericApiView/', genericAPIView.as_view()),
    path('GenericApiView/<int:id>/', genericAPIView.as_view()),
    path('',include(router.urls)),
]
