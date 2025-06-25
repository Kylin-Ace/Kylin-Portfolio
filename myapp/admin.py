from django.contrib import admin
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Project, BlogPost, About

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_featured', 'created_at')
    list_filter = ('is_featured',)
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'created_at', 'published_at')
    list_filter = ('status',)
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'published_at'
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if not change and obj.status == BlogPost.PUBLISHED:
            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)

@admin.register(About)
class AboutAdmin(admin.ModelAdmin):
    list_display = ('get_name', 'get_title', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'title', 'bio', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_name(self, obj):
        return obj.name if obj else '-'
    get_name.short_description = 'Name'

    def get_title(self, obj):
        return obj.title if obj else '-'
    get_title.short_description = 'Title'

    def has_add_permission(self, request):
        # Only allow adding if no About instance exists
        return not About.objects.exists()

    def has_delete_permission(self, request, obj=None):
        # Prevent deletion of the only instance
        return About.objects.count() > 1

    def save_model(self, request, obj, form, change):
        try:
            super().save_model(request, obj, form, change)
            if not change:
                messages.success(request, 'About information created successfully.')
            else:
                messages.success(request, 'About information updated successfully.')
        except ValidationError as e:
            messages.error(request, str(e))

    class Media:
        css = {
            'all': ('css/admin/about.css',)
        }
        js = ('js/admin/about.js',)