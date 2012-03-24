from django.contrib import admin
from blogs.models import Blog, Tag, Post


admin.site.register(Blog)
admin.site.register(Tag)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'is_public')
    list_display_links = ('title',)
    list_per_page = 50
    ordering = ['-created_at']
    search_fields = ['title', 'slug', 'body']

    fieldsets = (
        ('Title', {'fields':['title', 'tags', 'blog']}),
        ('Body', {'fields':['body']}),
        ('Publishing', {'fields':['is_public']}),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'blog':
            kwargs['empty_label'] = None
        return super(PostAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

admin.site.register(Post, PostAdmin)
