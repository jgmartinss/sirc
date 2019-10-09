from django.contrib.admin.apps import AdminConfig

from .admin import SircAdminSite


class SircAdminConfig(AdminConfig):
    default_site = "sirc.admin.SircAdminSite"
