from django.urls import path, include
from rest_framework import routers, serializers, viewsets

from api.v3.course import CourseViewSet, SectionViewSet, ActivityViewSet
from api.v3.tag import TagViewSet


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'course', CourseViewSet)
router.register(r'tag', TagViewSet)
router.register(r'section', SectionViewSet)
router.register(r'activity', ActivityViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls))
]