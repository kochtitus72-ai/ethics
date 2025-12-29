# articles/views.py
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ArticleForm
from .models import Article


def article_list(request):
    articles = Article.objects.all()
    return render(request, "articles/article_list.html", {"articles": articles})


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
