# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from ckeditor.fields import RichTextField

# Create your models here.
class Article(models.Model):
    class Meta():
        db_table = "article"
    article_title = models.CharField(max_length = 200)
    article_text = RichTextField()
    article_date = models.DateTimeField()
    article_likes = models.IntegerField(default=0)
    article_image = models.ImageField(null=True, blank=True, upload_to="images/", verbose_name= 'Изображение')

    def __unicode__(self):
        return self.article_title

    def bit(self):
        if self.article_image:
            return mark_safe ('<img src="%s" width="70"/>'% self.article_image.url)
        else:
            return '(none)'

    bit.short_descriptio = 'Изображение'
    bit.allow_tags = True


class Comments(models.Model):
    class Meta():
        db_table = 'comments'

    comments_text = models.TextField(verbose_name="Текст комментария")
    comments_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comments_date = models.DateField('date',auto_now=True)
    comments_author = models.ForeignKey(User, on_delete=models.CASCADE)