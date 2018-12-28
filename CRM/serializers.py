from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Company, Skill, Master, Order, Service
from rest_framework.fields import CurrentUserDefault


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(default="defaultpass")

    class Meta:
        model = User
        fields = "url", "username", "email", "groups", "password"
        extra_kwargs = {"password": {"write_only": True}}


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = "__all__"


class OptionsSerializer(serializers.Serializer):
    master = serializers.CharField(source="master__user__username")
    price = serializers.IntegerField()

    class Meta:
        fields = "master", "price"


class SkillSerializer(serializers.ModelSerializer):
    options = OptionsSerializer(many=True)

    class Meta:
        model = Skill
        fields = "id", "name", "options", "average_price"


class CatalogSerializer(serializers.Serializer):
    skill = serializers.CharField(source="skill__name")
    price = serializers.IntegerField()

    class Meta:
        fields = "skill", "price"


class MasterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="user.username", read_only=True)
    catalog = CatalogSerializer(many=True)
    average_price = serializers.IntegerField()

    class Meta:
        model = Master
        fields = "id", "name", "catalog", "average_price"


class PersonnelSerializer(serializers.Serializer):
    user__username = serializers.CharField()
    skills = serializers.IntegerField()


class ServiceSerializer(serializers.ModelSerializer):
    skill = serializers.CharField(source="skill.name")
    master = serializers.CharField(source="master.user.username")

    class Meta:
        model = Service
        fields = "id", "skill", "master", "price"


class OrderSerializer(serializers.ModelSerializer):
    client = serializers.CharField(default=serializers.CurrentUserDefault())
    service = serializers.CharField(source="service.skill.name")
    price = serializers.IntegerField(source="service.price")
    master = serializers.CharField(source="service.master")
    created = serializers.CharField(source="creation_date")

    class Meta:
        model = Order
        fields = ("client", "service", "master", "price", "created", "execution_date")
        extra_kwargs = {"executor": {"required": True, "label": "Master"}}

