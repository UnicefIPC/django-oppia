from rest_framework import routers, serializers, viewsets

from oppia.models import Tag


class TagSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Tag
        fields = ['url',
                  'id',
                  'name',
                  'description',
                  'highlight',
                  'icon',
                  'order_priority']


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    http_method_names = ['get']