from django.contrib import admin
from .models import Lead, Agent, User, UserProfile, Category


admin.site.register(User)
admin.site.register(Category)
admin.site.register(UserProfile)
admin.site.register(Agent)
admin.site.register(Lead)

# Register your models here.
