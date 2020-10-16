from rest_framework import routers, serializers, viewsets

from oppia.models import Course, Section, Activity


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

class CourseListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Course
        fields = ['url',
                  'title',
                  'version',
                  'shortname',
                  'priority',
                  'is_draft',
                  'description',
                  'sections']
        
    sections = SectionSerializer(many=True)

class CourseItemSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Course
        fields = ['url',
                  'title',
                  'version',
                  'shortname',
                  'priority',
                  'is_draft',
                  'description']

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.filter(is_archived=False, is_draft=False)
    http_method_names = ['get']

    def __init__(self, *args, **kwargs):
        super(CourseViewSet, self).__init__(*args, **kwargs)
        self.serializer_action_classes = {
            'list': CourseItemSerializer,
            'create': CourseListSerializer,
            'retrieve': CourseListSerializer,
            'update': CourseListSerializer,
            'partial_update': CourseListSerializer,
            'destroy': CourseListSerializer,
        }
        
    def get_serializer_class(self, *args, **kwargs):
        """Instantiate the list of serializers per action from class attribute (must be defined)."""
        kwargs['partial'] = True
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(CourseViewSet, self).get_serializer_class()

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.filter(course__is_archived=False, course__is_draft=False)
    serializer_class = SectionSerializer
    http_method_names = ['get']


class ActivityViewSet(viewsets.ModelViewSet):
    queryset = Activity.objects.filter(section__course__is_archived=False,
                                       section__course__is_draft=False)
    serializer_class = ActivitySerializer
    http_method_names = ['get']
