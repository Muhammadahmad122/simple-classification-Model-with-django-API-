from django.urls import path
from . import views
from . views import process_file
from .views import upload_file_view, process_file


urlpatterns = [
    path('upload/', upload_file_view, name='upload_file'),
    path('process-file/', process_file, name='process_file'),
]

