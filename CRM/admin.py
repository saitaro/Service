from django.contrib import admin
from .models import Company, Skill, Order, Master

# Register your models here.
admin.site.register(Company)
admin.site.register(Skill)
admin.site.register(Master)
admin.site.register(Order)

