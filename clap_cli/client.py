import requests
from typing import Optional, Dict


class ClapClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url.rstrip("/")

    def download_package(self, name: str, version: Optional[str]) -> requests.Response:
        url = f"{self.base_url}/package/download/{name}/"
        if version:
            url += f"{version}/"
        response = requests.get(url)
        response.raise_for_status()
        return response
    
    def info_package(self, name: str, version: Optional[str]) -> Dict[str, str]:
        url = f"{self.base_url}/package/info/{name}/"
        if version:
            url += f"{version}/"
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    