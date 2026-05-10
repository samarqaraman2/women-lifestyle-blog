from django.contrib import admin
from .models import Comment, Contact, Profile, Article
from .models import SiteSettings  

from django.utils.translation import gettext_lazy as _


class MyAdminSite(admin.AdminSite):
    site_header = "لوحة التحكم"
    site_title = "الإدارة"
    index_title = "مرحبًا بكِ في لوحة التحكم 💖"

    def each_context(self, request):
        context = super().each_context(request)
        context['custom_css'] = 'admin/custom_admin.css'
        return context


admin.site = MyAdminSite()

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Contact)
admin.site.register(Profile)

@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    list_display = ['site_name', 'maintenance_mode', 'contact_email']
