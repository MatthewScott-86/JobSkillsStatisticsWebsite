"""CS673_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from Site.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^database/', database),
    url(r'^indeed_database/', indeed_database),
    url(r'^glassdoor_database/', glassdoor_database),
    url(r'^county_choropleth/', county_choropleth),
    url(r'^indeed/', indeed),
    url(r'^glassdoor/',glassdoor),
    url(r'^tests/',tests),
    url(r'^plot/', Plot.as_view(), name='plotURL'),
    url(r'^indeed_compare/', indeed_compare),
    url(r'^$', landing_page),
]
