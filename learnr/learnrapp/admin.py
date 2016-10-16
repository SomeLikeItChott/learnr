from django.contrib import admin
from learnrapp.models import Message
from models import Problem

class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)
admin.site.register(Problem)
