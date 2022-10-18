from django.contrib import admin
from Home.models import CustomerRecord
# Register your models here.

class customerRecord(admin.ModelAdmin):
    list_display=["Name","City","ContactNo","Status"]

admin.site.register(CustomerRecord,customerRecord)