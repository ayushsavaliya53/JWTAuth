from django.contrib import admin
from .models import (
    image,
    OTPModel
)
from unfold.admin import ModelAdmin
from django.utils.html import format_html
from django.contrib.auth.models import User

# Register your models here.

class imageAdmin(ModelAdmin):
    list_display = ('image_name', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                f'<img src="{obj.image.url}" alt="Image could not be loaded." style="max-width:50px; height:auto;" />',
                
            )
        return "No image"
    def image_name(self, obj):
        return f'Image {obj.id}'

    image_preview.short_description = "Image Preview"

class UserAdmin(ModelAdmin):
    pass

class OTPAdmin(ModelAdmin):
    pass

admin.site.unregister(User)
admin.site.register(image, imageAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(OTPModel, OTPAdmin)

class CustomAdminClass(ModelAdmin):
    pass