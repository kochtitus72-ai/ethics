# articles/views.py
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArticleForm
from .models import Article
from django.db.models import Q   # import Q for flexible queries

# search feature added to this function on 31/12/2025
def article_list(request):
    query = request.GET.get("q")  # get ?q= from URL
    articles = Article.objects.all()

    if query:
        articles = articles.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(location__name__icontains=query) |
            Q(people__name__icontains=query)
        ).distinct()

    return render(request, "articles/article_list.html", {"articles": articles, "query": query})


def article_detail(request, public_id):
    article = get_object_or_404(Article, public_id=public_id)
    return render(request, "articles/article_detail.html", {"article": article})


def article_create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("article_list")
    else:
        form = ArticleForm()
    return render(request, "articles/article_form.html", {"form": form})


def article_update(request, public_id):
    article = get_object_or_404(Article, public_id=public_id)
    if request.method == "POST":
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect("article_detail", public_id=public_id)
    else:
        form = ArticleForm(instance=article)
    return render(request, "articles/article_form.html", {"form": form})


def article_delete(request, public_id):
    article = get_object_or_404(Article, public_id=public_id)
    if request.method == "POST":
        article.delete()
        return redirect("article_list")
    return render(request, "articles/article_confirm_delete.html", {"article": article})
