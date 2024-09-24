from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from mlapi import views
from django.urls import path
from mlapi.views import upload_file_view, process_file

urlpatterns = [
    path('api/', include('mlapi.urls')),
    path('process-file/', views.process_file, name='process_file'),
    path('upload/', upload_file_view, name='upload_file'),
    path('', include('mlapi.urls')),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

