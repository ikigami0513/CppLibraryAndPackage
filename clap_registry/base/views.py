from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.views import View


class IndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "index.html")


class DocumentationView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "documentation.html")
    