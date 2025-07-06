import os
import uuid
from django.core.exceptions import ValidationError
from django.db import models


def validate_exe_file(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != ".exe":
        raise ValidationError('Only .exe files are allowed.')
    

def clap_upload_path(instance: 'ClapVersion', filename: str) -> str:
    safe_version = instance.version.replace(' ', '_')
    filename = f"clap-{safe_version}.exe"
    return os.path.join("claps/", filename)
    

class ClapVersion(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version = models.CharField(max_length=50)
    is_latest = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to=clap_upload_path)

    def __str__(self) -> str:
        return f"clap - {self.version}"
