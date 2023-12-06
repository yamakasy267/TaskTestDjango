"""
URL configuration for Test project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os
from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import include
from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
SchemaView = get_schema_view(
    openapi.Info(
        title='Bplex API',
        default_version='v1.1',
        description='АПИ продукта bplex',
        terms_of_service='',
        license=openapi.License(name='Proprietary'),
    ),
    public=True,
    permission_classes=[AllowAny]
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('MainApp.urls'))
]

if os.getenv('DEBUG').lower() == 'true':
    #urlpatterns += staticfiles_urlpatterns()
    urlpatterns += re_path(r'^api/v1/?$', TemplateView.as_view(template_name='swagger-ui.html',
                                                extra_context={'schema_url': 'openapi-schema'}), name='swagger-ui'),
    urlpatterns += re_path(r'^api/v1/schema(?P<format>\.json|\.yaml)$',
            SchemaView.without_ui(cache_timeout=0), name='api-schema-url'),

