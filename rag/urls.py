from django.contrib import admin
from django.urls import path
from .views import chat, home,upload_document

urlpatterns = [
    path('', home, name='homepage'),
    path('upload',upload_document,name='upload'),
    path('chat',chat,name='chat'),
    
    # path('getfeedback',feedback_ready,name='feedback_ready')
]