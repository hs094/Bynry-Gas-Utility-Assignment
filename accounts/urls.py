from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('customers', views.CustomerProfileViewSet)
router.register('representatives', views.SupportRepresentativeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
