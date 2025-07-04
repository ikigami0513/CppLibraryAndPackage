from django.shortcuts import render
from django.views import View
from django.urls import reverse
from django.http import FileResponse, Http404, HttpRequest, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from .models import ClapVersion
from typing import Optional


class ClapVersionDownload(View):
    def get(self, request: HttpRequest, version: Optional[str] = None) -> FileResponse:
        if version:
            try:
                cv = ClapVersion.objects.get(version=version)
            except ClapVersion.DoesNotExist:
                raise Http404(f"Version '{version}' of clap not found.")
        else:
            try:
                cv = ClapVersion.objects.get(is_latest=True)
            except ClapVersion.DoesNotExist:
                raise Http404(f"Version '{version}' of clap not found.")
            
        if not cv.file or not cv.file.path:
            raise Http404("No file associated with this version of Clap.")
        
        return FileResponse(cv.file.open('rb'), as_attachment=True, filename=cv.file.name)
    