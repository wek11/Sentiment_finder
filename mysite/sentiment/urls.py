from django.urls import path, re_path
from . import views
from django.conf.urls.static import static
from django.conf import settings

app_name = 'sentiment'

# Configures urls for the sentiment project
urlpatterns = [
    path("results/<int:index>/", views.show_results, name="show-results"),
    path("", views.index, name="index"),
    path("index/", views.url_display, name="link-view"),
    re_path(r'^delete/(?P<pk>[0-9]+)$', views.delete_link, name='delete_link'), # Path to delete links using special link verbage
    
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # Loads static file directory