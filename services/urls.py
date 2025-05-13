from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = DefaultRouter()
router.register('types', views.ServiceTypeViewSet)
router.register('requests', views.ServiceRequestViewSet)

# Nested router for service request comments
requests_router = routers.NestedSimpleRouter(
    router,
    r'requests',
    lookup='service_request'
)
requests_router.register(
    r'comments',
    views.ServiceRequestCommentViewSet,
    basename='service-request-comments'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(requests_router.urls)),
]
