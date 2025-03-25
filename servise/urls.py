from django.urls import path
from . import views

urlpatterns = [

    path('', views.image_tool, name="image_tool"),
    path('converter/', views.converter, name="converter"),
    path('convertAll/', views.convertAll, name="convertAll"),
    path('image_to_pdf/', views.image_to_pdf, name="image_to_pdf"),
    path('upload_image/', views.upload_image, name="upload_image")

    ]