from django.contrib import admin

from .models import Page, Section

class SectionInline(admin.StackedInline):
	model = Section
	fields = ['title', 'order', 'body']
	extra = 1

class PageAdmin(admin.ModelAdmin):
	inlines = [SectionInline]

	class Meta:
		model = Page
		fields = ['title', 'order', 'body']

admin.site.register(Page, PageAdmin)
