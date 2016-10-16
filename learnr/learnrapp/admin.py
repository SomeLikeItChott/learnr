from django.contrib import admin
from learnrapp.models import Message, PublicUser, Problem

class MessageAdmin(admin.ModelAdmin):
    pass
admin.site.register(Message, MessageAdmin)

class PublicUserAdmin(admin.ModelAdmin):
    pass
admin.site.register(PublicUser, PublicUserAdmin)
admin.site.register(Problem)
