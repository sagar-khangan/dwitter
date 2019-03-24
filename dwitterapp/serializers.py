from rest_framework.serializers import ModelSerializer
from .models import DweetComments,Dweeter,Dweets
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username')


class DweetsSerializer(ModelSerializer):

    class Meta:
        model = Dweets
        fields = '__all__'


class DweeterSerializer(ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Dweeter
        fields = ('id','user','follows')


class DweeterCreateSerializer(ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = Dweeter
        fields = ('id','user','follows')

    def create(self, validated_data):
        user = User.objects.create_user(username = self.initial_data['user']['username'],email=None,password=self.initial_data['user']['password'])
        instance = Dweeter.objects.create(user=user)
        return instance


class DweetCommentSerializer(ModelSerializer):

    class Meta:
        model = DweetComments
        fields = '__all__'
