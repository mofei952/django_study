from django.contrib import admin

# Register your models here.
from app1.models import Article, Author, AuthorDetail, Publisher, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    # listdisplay设置要显示在列表中的字段（id字段是Django模型的默认主键）
    list_display = ('id', 'name', 'age', 'sex')

    search_fields = ('name', 'age', 'sex')

    list_filter = ('name', )

    # ordering设置默认排序字段，负号表示降序排序
    ordering = ('-age',)

    # fields = ('name', )

    # exclude = ('sex',)

    fieldsets = (
        (None, {
            'fields': ('name', 'sex')
        }),
        ('Advanced options', {
            'classes': ('collapse', ),
            'fields': ('age',)
        }),
    )

    # list_per_page设置每页显示多少条记录，默认是100条
    list_per_page = 50

    # list_editable 设置默认可编辑字段
    # list_editable = ['name', 'age', 'sex']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content', 'url', 'portal', 'author')

    # list_editable 设置默认可编辑字段
    # list_editable = ['title']


admin.site.register(AuthorDetail)
admin.site.register(Publisher)
admin.site.register(Book)
