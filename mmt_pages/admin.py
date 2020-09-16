from django.contrib import admin

from .models import Page

class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

	class Meta:
		model = Page

admin.site.register(Page, PageAdmin)
