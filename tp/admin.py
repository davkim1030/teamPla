from django.contrib import admin

# Register your models here.
from tp.models import *

admin.site.register(Team)
admin.site.register(Client)
admin.site.register(Project)