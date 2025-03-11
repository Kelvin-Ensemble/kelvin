from django.apps import AppConfig
from constance.apps import ConstanceConfig

class WebsiteConfig(AppConfig):
    name = "website"
    
class CustomConstance(ConstanceConfig):
    verbose_name = "Configuration"