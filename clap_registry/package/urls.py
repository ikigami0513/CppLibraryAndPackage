from django.urls import path
from . import views


urlpatterns = [
    path('', views.PackageListView.as_view(), name='package_list'),
    path('<str:package_name>/', views.PackageDetailView.as_view(), name='package_detail'),
    path('info/<str:package_name>/', views.PackageInfoView.as_view(), name='info_latest'),
    path('info/<str:package_name>/<str:version>/', views.PackageInfoView.as_view(), name='info_specific'),
    path('download/<str:package_name>/', views.PackageDownloadView.as_view(), name='download_latest'),
    path('download/<str:package_name>/<str:version>/', views.PackageDownloadView.as_view(), name='download_specific')
]
