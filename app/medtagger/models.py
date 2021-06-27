from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.search import SearchVectorField, SearchVector

# Create your models here.

class Journal(models.Model):

    ISSN = models.CharField(max_length=16)
    Title = models.CharField(max_length=256)
    ISOAbbreviation = models.CharField(max_length=256)

    def __str__(self):
        return self.Title


class Author(models.Model):

    LastName = models.CharField(max_length=128)
    ForeName = models.CharField(max_length=128, null=True)
    Initials = models.CharField(max_length=8)

    def __str__(self):
        return self.ForeName + ' ' + self.LastName


class Keyword(models.Model):

    KeywordText = models.TextField(max_length=64)

    def __str__(self):
        return self.KeywordText


class Tag(models.Model):
    WikiID = models.CharField(max_length=64)
    Label = models.CharField(max_length=64)
    Description = models.TextField(max_length=1024, null=True)
    # Maybe an array field for tokens?
    Tokens = models.TextField(max_length=1024, null=True)
    SearchIndex = SearchVectorField(null=True)

    def createTSvector(self, *args, **kwargs):
        self.SearchIndex = (
                SearchVector('Label', weight='A')
                + SearchVector('Tokens', weight='B')
                + SearchVector('Description', weight='C')
        )
        super().save(*args, **kwargs)


class Article(models.Model):

    PMID = models.CharField(max_length=16)
    Title = models.TextField(max_length=512)
    Abstract = models.TextField(max_length=5000, null=True)
    PublicationDate = models.DateField(null=True)

    Journal = models.ForeignKey(Journal, on_delete=models.PROTECT, null=True)
    Keywords = models.ManyToManyField(Keyword)
    Authors = models.ManyToManyField(Author)
    Tags = models.ManyToManyField(Tag)

    # Tokens = ArrayField(
    #     models.CharField(max_length=128),
    #     size=128
    # )

    Tokens = models.TextField(max_length=100000)

    SearchIndex = SearchVectorField(null=True)

    def createTSvector(self, *args, **kwargs):
        self.SearchIndex = (
                SearchVector('PMID', weight='A')
                + SearchVector('Title', weight='A')
                + SearchVector('Abstract', weight='B')
                + SearchVector('Tokens', weight='C')
        )
        super().save(*args, **kwargs)

    def __str__(self):
        return self.Title


