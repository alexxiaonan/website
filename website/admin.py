from django.contrib import admin
from .models import Record, Communication_Record, Group_Record, Sender


# Register your models here.
admin.site.register([Record, Communication_Record, Group_Record, Sender])
