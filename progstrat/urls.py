"""progstrat URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from rest_framework import urls as rest_urls

from progstrat.router import router
from progstrat import views as base_views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include(rest_urls, namespace='rest_framework')),
    url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'^landing/$', base_views.landing, name='landing'),
    url(r'^login/$', base_views.login, name='login'),
    url(r'^logout/$', base_views.logout_user, name='logout'),
    url(r'^$', base_views.home, name='home'),

    url(r'^passwd/reset/$', 'django.contrib.auth.views.password_reset'),
    url(r'^passwd/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^passwd/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm'),
    url(r'^passwd/reset/complete/$', 'django.contrib.auth.views.password_reset_complete'),
    url(r'^passwd/change/$', 'django.contrib.auth.views.password_change'),
    url(r'^passwd/change/done/$', 'django.contrib.auth.views.password_change_done'),

    url(r'^robots\.txt$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name="robots"),
    url(r'^humans\.txt$', TemplateView.as_view(template_name='humans.txt', content_type='text/plain'), name="humans"),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # pragma: no cover
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # pragma: no cover




