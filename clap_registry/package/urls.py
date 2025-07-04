from django.urls import path
from .views import PackageDownloadView, PackageInfoView, PackageListView


urlpatterns = [
    path('', PackageListView.as_view(), name='package_list'),
    path('info/<str:package_name>/', PackageInfoView.as_view(), name='info_latest'),
    path('info/<str:package_name>/<str:version>/', PackageInfoView.as_view(), name='info_specific'),
    path('download/<str:package_name>/', PackageDownloadView.as_view(), name='download_latest'),
    path('download/<str:package_name>/<str:version>/', PackageDownloadView.as_view(), name='download_specific')
]
