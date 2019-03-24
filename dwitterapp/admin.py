from django.contrib import admin
from .models import Dweeter,Dweets,DweetComments
# Register your models here.

admin.site.register(Dweets)
admin.site.register(Dweeter)
admin.site.register(DweetComments)
