from django.test import TestCase
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from . import views
from .views import index, articleDetails, tags, TagAutocomplete


class TestUrls(SimpleTestCase):

    def test_index_url_is_resolved(self):
        url = reverse('index')
        print(resolve(url))
        self.assertEquals(resolve(url).func, index)

    def test_articleDetails_url_is_resolved(self):
        url = reverse('articleDetails', args=[1])
        print(resolve(url))
        self.assertEquals(resolve(url).func, articleDetails)

    def test_tags_url_is_resolved(self):
        url = reverse('tags')
        print(resolve(url))
        self.assertEquals(resolve(url).func, tags)

    def test_tagautocomplete_url_is_resolved(self):
        url = reverse('tag-autocomplete')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, TagAutocomplete)

