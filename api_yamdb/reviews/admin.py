from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title

admin.site.register(Title)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)

    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}
