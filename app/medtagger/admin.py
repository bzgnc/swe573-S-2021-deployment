from django.contrib import admin
from medtagger.models import Journal, Author, Keyword, Tag, Article

# Register your models here.
myModels = [Journal, Author, Keyword, Tag, Article]
admin.site.register(myModels)
