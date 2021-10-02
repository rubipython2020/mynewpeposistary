from django.contrib import admin

from .models import Post,Profile,Comment

class AdminPost(admin.ModelAdmin):
    list_display = ['title','slug','body','author','created','updated','status']
    prepopulated_fields = {'slug':('title',)}
    list_editable = ('status',)
class AdminProfile(admin.ModelAdmin):
    list_display = ['user','dob','phote']

admin.site.register(Post,AdminPost)
admin.site.register(Profile,AdminProfile)
admin.site.register(Comment)