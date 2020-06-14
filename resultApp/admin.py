from django.contrib import admin

# Register your models here.
from resultApp.models import *

admin.site.register(Student)
admin.site.register(Marks)
admin.site.register(Carryover)
admin.site.register(Visitor)
