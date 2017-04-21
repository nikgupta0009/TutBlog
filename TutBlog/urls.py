"""TutBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
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
from django.conf.urls import url, include
from django.conf import settings
from django.contrib import admin
from User.forms import LoginForm
from django.contrib.auth import views
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login, {'template_name': 'login.html', 'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', views.logout, {'next_page': '/login'}),
    url(r'^summernote/', include('django_summernote.urls')),
    url(r'^blogs/', include('Blogs.urls')),
    url(r'', include('User.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
if settings.DEBUG:
   urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
