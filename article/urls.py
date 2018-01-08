from django.urls import path, include,re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('1/', views.basic_one),
    path('2/', views.template_two),
    path('3/', views.template_three_simple),
    path('articles/all/', views.articles),
    path('articles/get/<int:article_id>/', views.article),
    re_path(r'^articles/(?P<article_id>\d+)/get/(?P<page_comments_number>\d+)/$', views.article),
    re_path(r'^articles/addlike/(?P<article_id>\d+)/$', views.addlike),
    #re_path(r'^articles/addlike/(?P<article_id>\d+)/$', views.addlike),
    #path('articles/addlike/<int:article_id>/', views.addlike),
    path('articles/addcomment/<int:article_id>/', views.addcomment),
    re_path(r'^page/(\d+)/$', views.articles),
    path('', views.articles),


]
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns() + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)