from django.contrib import admin

# Register your models here.
from .models import Students, Marks, Carryover

admin.site.register(Students)
admin.site.register(Marks)
admin.site.register(Carryover)