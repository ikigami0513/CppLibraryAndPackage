from django.contrib import admin
from .models import Package, VersionPackage


class VersionPackageInline(admin.TabularInline):
    model = VersionPackage
    extra = 0


@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]
    inlines = [VersionPackageInline]


@admin.register(VersionPackage)
class VersionPackageAdmin(admin.ModelAdmin):
    list_display = ["package", "version", "is_latest", "uploaded_at"]
