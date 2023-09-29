from django.contrib import admin

from .models import Page, Section

class SectionInline(admin.StackedInline):
	model = Section
	prepopulated_fields = {"slug": ("title",)}
	fields = ['title', 'slug', 'order', 'body',]
	extra = 1

class PageAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('title',)}

	inlines = [SectionInline]

	class Meta:
		model = Page

admin.site.register(Page, PageAdmin)
