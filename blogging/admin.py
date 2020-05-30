from django.contrib import admin
from blogging.models import Post, Category


class CategoryInline(admin.TabularInline):
    model = Category.posts.through


class CategoryAdmin(admin.ModelAdmin):
    exclude = ["posts"]


class PostAdmin(admin.ModelAdmin):
    date_hierarchy = "published_date"
    actions_selection_counter = True
    inlines = [CategoryInline]
    # Not quite sure what qualifies as 'custom' here.


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
