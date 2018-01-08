from django.shortcuts import render
from django.http.response import HttpResponse, Http404
from django.template.loader import get_template
from django.shortcuts import render_to_response, redirect
from article.models import Article, Comments
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from article.forms import CommentForm
from django.template.context_processors import csrf
from django.contrib import auth

# Create your views here.

def basic_one(request):
    view = "basic_one"
    html = "<html><body>This is %s view</html></body>" %view
    return HttpResponse(html)

def template_two(request):
    view = "template_two"
    t = get_template('myview.html')
    html = t.render({'name': view})
    return HttpResponse(html)

def template_three_simple(request):
    view = "template_three"
    return render_to_response('myview.html', {'name': view})

def articles(request, page_number=1):
    all_articles = Article.objects.all()
    current_page = Paginator(all_articles, 2)
    return render_to_response('articles.html', {'articles': current_page.page(page_number), 'username': auth.get_user(request).username})


def article(request, page_comments_number=1, article_id=1):
    comment_form = CommentForm
    all_comments = Comments.objects.all()
    args = {}
    args.update(csrf(request))
    args['article'] = Article.objects.get(id=article_id)
    current_page_comments_filter = all_comments.filter(comments_article_id=article_id)
    current_page_comments = Paginator(current_page_comments_filter, 4)
    args['comments'] = current_page_comments.page(page_comments_number)
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username
    return render_to_response('article.html', args)


"""def article(request, article_id=1):
    comment_form = CommentForm
    args = {}
    args.update(csrf(request))
    args['article'] = Article.objects.get(id=article_id)
    args['comments'] = Comments.objects.filter(comments_article_id=article_id)
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username
    return render_to_response('article.html', args)"""


def addlike(request, article_id):
    back_url = request.META['HTTP_REFERER']
    try:
        if article_id in request.COOKIES:
            redirect(back_url)
        else:
            article = Article.objects.get(id=article_id)
            article.article_likes += 1
            article.save()
            return_path = request.META.get('HTTP_REFERER', '/')
            response = redirect(return_path)
            response.set_cookie(article_id, 'value')
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect(back_url)


"""def addlike(request, article_id):
    try:
        if article_id in request.COOKIES:
            redirect('/')
        else:
            article = Article.objects.get(id=article_id)
            article.article_likes += 1
            article.save()
            response = redirect('/')
            response.set_cookie(article_id, "test")
            return response
    except ObjectDoesNotExist:
        raise Http404
    return redirect('/')"""

def addcomment(request, article_id):
    if request.POST and ("pause" not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_author = request.user
            comment.comments_article = Article.objects.get(id=article_id)
            form.save()
            request.session.set_expiry(60)
            request.session['pause'] = True
    return redirect('/articles/get/%s/' % article_id)