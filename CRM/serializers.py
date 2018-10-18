from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Company, Skill, Master, Order
from rest_framework.fields import CurrentUserDefault


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = 'url', 'username', 'email', 'groups'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'

    def to_representation(self):
        return 'pooook'
        

class MasterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Master
        fields = 'pk', 'user', 'skills', 'url'


class OrderSerializer(serializers.ModelSerializer):
    client = serializers.CharField(default=serializers.CurrentUserDefault())
    executor_name = serializers.CharField(source='executor.user.username', read_only=True)
    service_name = serializers.CharField(source='service.name', read_only=True)

    class Meta:
        model = Order
        fields = ('client', 'service', 'service_name', 'executor',
                  'executor_name', 'execution_date')
        extra_kwargs = {
            'executor': {'required': True, 'label': 'master_id'},
            # 'service': {'required': True},
        }


