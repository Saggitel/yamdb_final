from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class GenreAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class TitleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class CommentAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


class ReviewAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    pass


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Review, ReviewAdmin)
