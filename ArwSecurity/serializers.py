from rest_framework import serializers

from ArwSecurity.models import product
from django.contrib.auth.models import User, Group


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    #  user = serializers.HyperlinkedRelatedField(many=True, view_name='group-detail', read_only=True)

    class Meta:
        model = product
        fields = ('name', 'description', 'price', 'info', 'image')
