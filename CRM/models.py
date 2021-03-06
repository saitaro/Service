from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg, OuterRef, Q, Subquery
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class Company(models.Model):
    name = models.CharField(max_length=127)

    class Meta:
        verbose_name_plural = 'Companies'

    def __str__(self):
        return self.name

    def service(self):
        return self.masters.select_related('skills', 'name') \
                           .values_list('skills__name', flat=True).distinct()


class Skill(models.Model):
    name = models.CharField(max_length=127, blank=False)

    @property
    def options(self):
        return Service.objects.filter(skill=self.pk).values('master__user__username', 
                                                            'price')
    @property
    def average_price(self):
        return self.options.aggregate(avg=Avg('price'))['avg']

    def __str__(self):
        return self.name


class Master(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField('Skill', through='Service', related_name='masters')
    company = models.ForeignKey('Company', related_name='masters', null=True, 
                                on_delete=models.SET_NULL)

    class Meta:
        verbose_name_plural = 'masters'

    @classmethod
    def averages(cls):
        queryset = Master.objects.all()
        return {master: master.average_price for master in queryset}

    @property 
    def average_price(self):
        return self.catalog.aggregate(Avg('price'))['price__avg']

    @property
    def catalog(self):
        return Service.objects.filter(master=self.pk).values('skill__name', 'price')

    def __str__(self):
        return self.user.username


# @receiver(post_save, sender=Master)
# def add_to_group(sender, instance, created, **kwargs):
#     if created:
#         instance.groups.add(Group.objects.get(name='Masters'))


class Service(models.Model):
    master = models.ForeignKey('Master', related_name='services', on_delete=models.CASCADE)
    skill = models.ForeignKey('Skill', related_name='skills', on_delete=models.CASCADE,
                              blank=True, null=True)
    price = models.PositiveIntegerField(blank=True, null=True)
    task_time = models.DurationField(blank=True, null=True)

    @classmethod
    def catalog(cls, skill=None):
        if skill:
            return Skill.objects.get(name=skill).average_price
        else:
            return {skill.name: skill.average_price for skill in Skill.objects.all()}

    def __str__(self):
        return f'{self.skill.name} by {self.master.user.username}'


class Order(models.Model):
    client = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', related_name='orders', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    execution_date = models.DateTimeField(blank=False)

    def __str__(self):
        return f'{self.pk} – {self.service} for {self.client}'
