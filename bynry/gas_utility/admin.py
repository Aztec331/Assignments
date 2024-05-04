from django.contrib import admin
from .models import User,Service,Category

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Service)
