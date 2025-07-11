from django.contrib import admin
from .models import Pays, Destination, Hebergement, Utilisateur, Reservation, Blog, Commentaire
from django.utils.html import format_html

# Register your models here.
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('nom', 'pays', 'photo_tag')
    readonly_fields = ('photo_tag',)
    def photo_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:60px;max-width:100px;" />', obj.photo.url)
        return ""
    photo_tag.short_description = 'Photo'

class HebergementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'destination', 'type', 'photo_tag')
    readonly_fields = ('photo_tag',)
    def photo_tag(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="max-height:60px;max-width:100px;" />', obj.photo.url)
        return ""
    photo_tag.short_description = 'Photo'

admin.site.register(Destination, DestinationAdmin)
admin.site.register(Hebergement, HebergementAdmin)
admin.site.register(Pays)
admin.site.register(Utilisateur)
admin.site.register(Reservation)
admin.site.register(Blog)
admin.site.register(Commentaire)
