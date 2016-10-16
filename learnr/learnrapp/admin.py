from django.contrib import admin
from learnrapp.models import Message

class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)