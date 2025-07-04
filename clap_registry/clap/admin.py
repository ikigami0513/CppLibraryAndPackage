from django.contrib import admin
from .models import *


@admin.register(ClapVersion)
class ClapVersionAdmin(admin.ModelAdmin):
    list_display = ["version", "is_latest", "uploaded_at"]
