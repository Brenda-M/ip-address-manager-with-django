from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import *

urlpatterns = [
  path('', home, name='home'),
  path('ip/available', list_available_ips, name='list_available_ips'),
  path('ip/allocated', list_allocated_ips, name='list_allocated_ips'),
  path('ip/release/<str:ip_address>', release_ip_address, name='release_ip_address'),
  path('ip/allocate', allocate_ip_address, name='allocate_ip_address'),
  path('ip/subnet_calculator', subnet_calculator, name='subnet_calculator'),
  path('filter-ips-by-range/', filter_ips_by_range, name='filter_ips_by_range'),
  path('ip/unreserve/<str:ip_address>', unreserve_ip_address, name='unreserve_ip_address'),
]


if settings.DEBUG:
  urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)