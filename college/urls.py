
from django.contrib import admin
from django.urls import path
from collageApp import views

urlpatterns = [

    path('admin/', admin.site.urls),
    #path('index', views.index),
    path('', views.home),

    path('update/', views.update),
    path('marks_update/', views.marks_update),
    path('class_rank/', views.class_rank),
    path('class_rank/<int:flag>', views.class_rank),
]
