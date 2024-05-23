from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'sentiment'

urlpatterns = [
    path("results/<int:index>/", views.show_results, name="show-results"),
    path("", views.index, name="index"),
    path("index/", views.url_display, name="link-view"),
    re_path(r'^delete/(?P<pk>[0-9]+)$', views.delete_link, name='delete_link'),
    
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)