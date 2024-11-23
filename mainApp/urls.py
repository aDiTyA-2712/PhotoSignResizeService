from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet,upload_images,upload_success

router=DefaultRouter()
router.register(r'images',ImageViewSet)

urlpatterns=[
    path('',include(router.urls)),
    path('upload/',upload_images,name='upload_images'),
    path('upload/success/',upload_success,name='upload_success')
]