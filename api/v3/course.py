
from django.contrib.auth.models import User

from rest_framework import routers, serializers, viewsets, pagination
from rest_framework.response import Response

from oppia.models import Course, Section, Activity


class CoursePagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'courses': data
        })

class ActivitySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Activity
        fields = ['url',
                  'title',
                  'order',
                  'type',
                  'digest']


class SectionSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Section
        fields = ['url',
                  'title',
                  'order',
                  'activities']
        
    activities = ActivitySerializer(many=True)


class AuthorSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ['first_name']


class CourseItemSerializer(serializers.HyperlinkedModelSerializer):
    
    author = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['url',
                  'title',
                  'version',
                  'shortname',
                  'priority',
                  'is_draft',
                  'description',
                  'sections',
                  'author',
                  'organisation']
        
    sections = SectionSerializer(many=True)
    
    def get_author(self, obj):
        return obj.user.first_name  + " " + obj.user.last_name

    def get_organisation(self, obj):
        return obj.user.userprofile.organisation


class CourseSerializer(serializers.HyperlinkedModelSerializer):

    author = serializers.SerializerMethodField()
    organisation = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['url',
                  'title',
                  'version',
                  'shortname',
                  'priority',
                  'is_draft',
                  'description',
                  'author',
                  'organisation']

    def get_author(self, obj):
        return obj.user.first_name  + " " + obj.user.last_name

    def get_organisation(self, obj):
        return obj.user.userprofile.organisation


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_archived=False, is_draft=False)
    http_method_names = ['get']
    pagination_class = CoursePagination

    def __init__(self, *args, **kwargs):
        super(CourseViewSet, self).__init__(*args, **kwargs)
        self.serializer_action_classes = {
            'list': CourseSerializer,
            'create': CourseSerializer,
            'retrieve': CourseItemSerializer,
            'update': CourseSerializer,
            'partial_update': CourseSerializer,
            'destroy': CourseSerializer,
        }
        
    def get_serializer_class(self, *args, **kwargs):
        kwargs['partial'] = True
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(CourseViewSet, self).get_serializer_class()


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.filter(course__is_archived=False,
                                      course__is_draft=False)
    serializer_class = SectionSerializer
    http_method_names = ['get']


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.filter(section__course__is_archived=False,
                                       section__course__is_draft=False)
    serializer_class = ActivitySerializer
    http_method_names = ['get']
