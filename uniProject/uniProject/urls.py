"""uniProject URL Configuration

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
from django.conf.urls.static import static
from django.conf import settings
from django.urls import include, path
from django.views.generic.base import RedirectView
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import TemplateView

handler404 = 'crawler.views.error_404'

urlpatterns = [
    path('', include('adminSection.urls')),
    path('', include('crawler.urls')),
    path('', include('pricePrediction.urls')),
    path('', include('materialStockApp.urls')),
    path("favicon.ico", RedirectView.as_view(url=staticfiles_storage.url("favicon.ico")),),
    path('contact/', TemplateView.as_view(template_name='contact.html')),
    path('learn/', TemplateView.as_view(template_name='learn.html')),
    path('contactThankYou/', TemplateView.as_view(template_name='contactThankYou.html'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
