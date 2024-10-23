from django.contrib import admin
from .models import Chunk, User
# Register your models here.
admin.site.register(User)
admin.site.register(Chunk)
# admin.site.register(User)