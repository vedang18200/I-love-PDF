from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('merge/', views.merge_pdfs_view, name='merge'),
    path('split/', views.split_pdfs_view, name='split'),
    path('compress/', views.compress_pdfs_view, name='compress'),
    path('convert/', views.convert_to_pdf_view, name='convert'),
]
