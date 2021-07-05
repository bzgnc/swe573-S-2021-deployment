from django.shortcuts import render
from functools import reduce
from dal import autocomplete
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.postgres.search import SearchQuery, SearchRank
from medtagger.forms import TagForm
from medtagger.models import Article, Author, Tag, Keyword
from medtagger.Wikiman import getLabelSuggestion, WikiEntry
from django.db.models import F, CharField, Value
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from medtagger.downloadArticles import getArticles


@login_required(login_url="/accounts/login/")
def index(request):
    if request.method == 'POST':
        search_terms = [SearchQuery(term, search_type='phrase') for term in request.POST.get('searchTerms').split(",")]
        article_search_query = reduce(lambda x, y: x & y, search_terms)
        tag_search_query = reduce(lambda x, y: x | y, search_terms)
        article_search_results = Article.objects. \
            filter(SearchIndex=article_search_query). \
            annotate(rank=SearchRank(F('SearchIndex'), article_search_query))
        tag_search_results = Article.objects. \
            filter(Tags__SearchIndex=tag_search_query). \
            annotate(rank=SearchRank(F('SearchIndex'), tag_search_query))
        results_list = (tag_search_results | article_search_results).distinct().order_by('-rank')
        page = request.POST.get('page', 1)
        paginator = Paginator(results_list, 25)
        search_str = request.POST.get('searchTerms')
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        # results_list = (article_search_results | tag_search_results).distinct().order_by('-rank')
        results_dict = {"results_list": results,
                        "search_term": search_str
                        }
        return render(request, 'results.html', context=results_dict)
    else:
        if request.GET.get('page', False):
            page = request.GET.get('page')
            search_terms = [SearchQuery(term, ) for term in request.GET.get('term').split(",")]
            article_search_query = reduce(lambda x, y: x & y, search_terms)
            tag_search_query = reduce(lambda x, y: x | y, search_terms)
            article_search_results = Article.objects. \
                filter(SearchIndex=article_search_query). \
                annotate(rank=SearchRank(F('SearchIndex'), article_search_query))
            tag_search_results = Article.objects. \
                filter(Tags__SearchIndex=tag_search_query). \
                annotate(rank=SearchRank(F('SearchIndex'), tag_search_query))
            results_list = (tag_search_results | article_search_results).distinct().order_by('-rank')
            paginator = Paginator(results_list, 25)
            search_str = request.GET.get('term')
            try:
                results = paginator.page(page)
            except PageNotAnInteger:
                results = paginator.page(1)
            except EmptyPage:
                results = paginator.page(paginator.num_pages)
            # results_list = (article_search_results | tag_search_results).distinct().order_by('-rank')
            results_dict = {"results_list": results,
                            "search_term": search_str
                            }
            return render(request, 'results.html', context=results_dict)
        else:
            return render(request, 'index.html')


def articleDetails(request, pk):
    article = Article.objects.get(pk=pk)
    if request.method == 'POST':
        if 'add_tag' in request.POST:
            tag_form = TagForm(data=request.POST)
            if tag_form.data['wikiLabel']:
                tag_data = WikiEntry(tag_form.data['wikiLabel'])
                tag, created = Tag.objects.get_or_create(WikiID=tag_data.getID(), Label=tag_data.getLabel())
                if created:
                    tag.Description = tag_data.getDescription()
                    tag.Tokens = tag_data.getTokens()
                    tag.save()
                    tag.createTSvector()
                    article.Tags.add(tag)
                else:
                    article.Tags.add(tag)
        elif 'tag_id' in request.POST:
            tag = Tag.objects.get(pk=request.POST['tag_id'])
            print(request.POST['tag_id'])
            article.Tags.remove(tag)

    tag_form = TagForm()
    authors = Author.objects.filter(article=article)
    keywords = Keyword.objects.filter(article=article)
    keywords_list = ', '.join([item.KeywordText for item in keywords])
    tags = Tag.objects.filter(article=article)
    article_dict = {"authors": authors,
                    "title": article.Title,
                    "abstract": article.Abstract,
                    "pmid": article.PMID,
                    "tag_form": tag_form,
                    "keywords": keywords_list,
                    "tags": tags
                    }

    return render(request, 'articleDetails.html', context=article_dict)


class TagAutocomplete(autocomplete.Select2ListView):

    def get_list(self):
        tags = getLabelSuggestion(self.q)
        return tags


def tags(request):
    tags = Tag.objects.all()

    return render(request, 'tags.html',
                  context={'tags': tags})

def theget(request):
    getArticles('catatonic schizophrenia', '10000')
    return HttpResponse('It is all ok!')

