import os
import uuid
from django.core.exceptions import ValidationError
from django.db import models


def validate_zip_file(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.zip':
        raise ValidationError('Only .zip files are allowed.')
    

def package_upload_path(instance: 'VersionPackage', filename: str) -> str:
    safe_name = instance.package.name.replace(' ', '_')
    safe_version = instance.version.replace(' ', '_')
    filename = f"{safe_name}-{safe_version}.zip"
    return os.path.join("packages", filename)


class Package(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    repository_url = models.URLField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    def latest(self) -> str:
        vp = VersionPackage.objects.get(package=self, is_latest=True)
        return vp.version
    
    class Meta:
        ordering = ["name"]


class VersionPackage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="versions")
    version = models.CharField(max_length=50)
    file = models.FileField(upload_to=package_upload_path, validators=[validate_zip_file])
    is_latest = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    target_library = models.CharField(max_length=500, null=True)

    def __str__(self) -> str:
        return f"{self.package} - {self.version}"
