from django.urls import path
from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name="index_view"),
    path('documentation/', views.DocumentationView.as_view(), name="documentation_view")
]
