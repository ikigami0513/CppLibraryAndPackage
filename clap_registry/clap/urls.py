from django.urls import path
from . import views


urlpatterns = [
    path('download/', views.ClapVersionDownload.as_view(), name='download_clap_latest'),
    path('download/<str:version>/', views.ClapVersionDownload.as_view(), name='download_clap_specific')
]
