from django.contrib import admin

# Register your models here.
from tp.models import *

admin.site.register(User)
admin.site.register(Project)
admin.site.register(Team)
