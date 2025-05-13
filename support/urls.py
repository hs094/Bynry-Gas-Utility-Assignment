from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from . import views

router = DefaultRouter()
router.register('tickets', views.SupportTicketViewSet)
router.register('interactions', views.CustomerInteractionViewSet)

# Nested router for support ticket interactions
tickets_router = routers.NestedSimpleRouter(
    router,
    r'tickets',
    lookup='support_ticket'
)
tickets_router.register(
    r'interactions',
    views.CustomerInteractionViewSet,
    basename='ticket-interactions'
)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(tickets_router.urls)),
]
