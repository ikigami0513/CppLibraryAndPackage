from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.http import FileResponse, Http404, HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import Package, VersionPackage
from typing import Optional


class PackageInfoView(View):
    def get(self, request: HttpRequest, package_name: str, version: Optional[str] = None) -> JsonResponse:
        package = get_object_or_404(Package, name=package_name)

        if version:
            try:
                vp = VersionPackage.objects.get(package=package, version=version)
            except VersionPackage.DoesNotExist:
                raise Http404(f"Version '{version}' not found for package '{package_name}'.")
        else:
            try:
                vp = VersionPackage.objects.get(package=package, is_latest=True)
            except VersionPackage.DoesNotExist:
                raise Http404(f"No latest version found for package '{package_name}'.")
            
        if not vp.file:
            raise Http404("No file associated with this version.")
        
        download_url = request.build_absolute_uri(
            reverse("download_specific", args=[package_name, vp.version])
        )

        return JsonResponse({
            "name": package.name,
            "version": vp.version,
            "download_url": download_url,
            "target_library": vp.target_library
        })


class PackageDownloadView(View):
    def get(self, request: HttpRequest, package_name: str, version: Optional[str] = None) -> FileResponse:
        package = get_object_or_404(Package, name=package_name)

        if version:
            try:
                vp = VersionPackage.objects.get(package=package, version=version)
            except VersionPackage.DoesNotExist:
                raise Http404(f"Version '{version}' not found for package '{package_name}'.")
        else:
            try:
                vp = VersionPackage.objects.get(package=package, is_latest=True)
            except VersionPackage.DoesNotExist:
                raise Http404(f"No latest version found for package '{package_name}'.")
            
        if not vp.file or not vp.file.path:
            raise Http404("No file associated with this version.")
        
        return FileResponse(vp.file.open('rb'), as_attachment=True, filename=vp.file.name)
    

class PackageListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        packages = Package.objects.all()
        return render(request, "packages.html", {
            "packages": packages
        })

