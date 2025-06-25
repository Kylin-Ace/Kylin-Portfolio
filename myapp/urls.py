from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.home, name='home'),
    path('project/<slug:slug>/', views.project_detail, name='project_detail'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
