
from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home ,name='home') ,
    #path('updateStudent', views.updateStudent ,name='updateStudent') ,
    #path('updateMarks', views.updateMarks ,name='updateMarks') ,
    path('fullResult', views.fullResult ,name='fullResult') ,
    path('fullResult/<str:rolln>', views.fullResult ,name='fullResult') ,
    path('classRank', views.classRank ,name='classRank') ,
    path('pdf/<str:batch>/<str:branch_code>/<str:year>', views.ViewPdf.as_view() ) ,
    #path('pdf/', views.ViewPdf.as_view() ,name='pdf') ,
    path('pdfDekho/', views.pdfDekho ,name='pdf') ,

    #path('classRank', views.classRank ,name='classRank') ,
]
