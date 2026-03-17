from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet

# Der Router erstellt automatisch Routen wie /api/boards/ und /api/boards/{id}/
router = DefaultRouter()
router.register(r'', BoardViewSet, basename='board')

urlpatterns = [
    path('', include(router.urls)),
]
