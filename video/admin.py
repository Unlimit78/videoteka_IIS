from django.contrib import admin

# Register your models here.
from .models import Genre,VideoCasets,User,Types

admin.site.register(VideoCasets)
admin.site.register(Genre)
admin.site.register(User)
admin.site.register(Types)
