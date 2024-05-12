from django.db import models
from django.db.models import Sum
from django.db.models.functions import Coalesce
from datetime import datetime
from .resources import TOPICS, politic, CONTENT, article
from django.contrib.auth.models import User
# Create your models here.


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    user_rating = models.IntegerField(default = 0)

    def update_rating(self):
        posts_rating = Post.objects.filter(author = self).aggregate(pr=Coalesce(Sum('post_rating'), 0))['pr'] #В переменной posts_rating создается словарь по умолчанию - {'post_rating__sum': -3}, pr=Sum() - создаем пользовательское название ключа для словаря - "pr" и потом обращаемся к нему - [pr]
        #через обратные отношения variant_3
        # posts_rating = self.post_set.aggregate(pr=Coalesce(Sum('post_rating'), 0))['pr']
        comments_rating = Comment.objects.filter(comment_user = self.user).aggregate(cr=Coalesce(Sum('comment_rating'), 0))['cr'] #с помощью coalesce ловим None и заменяем на необходимый нам паремтр, в нашем лсучае на ноль, чтоб можно было произвести агрегацию
        # comments_rating = self.user.comment_set.aggregate(cr=Coalesce(Sum('comment_rating'), 0))['cr']
        posts_comments_rating = Comment.objects.filter(comment_post__author = self).aggregate(pcr=Coalesce(Sum('comment_rating'), 0))['pcr']
        # posts_comments_rating = self.post_set.aggregate(pcr=Coalesce(Sum('comment__comment_rating'), 0)).get('pcr') получили данные из словаря с помощью метода гет

        #Variant_1
        # posts_rating = 0
        # comments_rating = 0
        # posts_comments_rating = 0
        #
        # posts = Post.objects.filter(author = self)
        # for p in posts:
        #     posts_rating += p.post_rating
        #
        # comments = Comment.objects.filter(comment_user = self.user)
        # for c in comments:
        #     comments_rating += c.comment_rating
        #
        # posts_comments = Comment.objects.filter(comment_post__author = self)
        # for pc in posts_comments:
        #     posts_comments_rating += pc.comment_rating
        print(f'posts_rating = {posts_rating}')
        print('--------------')
        print(f'comments_rating = {comments_rating}')
        print('--------------')
        print(f'posts_comments_rating = {posts_comments_rating}')
        self.user_rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()


class Category(models.Model):
    topic = models.CharField(max_length=2, choices=TOPICS, default=politic, unique=True)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    content = models.CharField(max_length=2, choices=CONTENT, default=article)
    date = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through = 'PostCategory')
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=10000)
    post_rating = models.IntegerField(default=0)

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    def preview(self):
        return self.text[:125]+"..."


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete = models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    comment_post = models.ForeignKey(Post, on_delete = models.CASCADE)
    comment_user = models.ForeignKey(User, on_delete = models.CASCADE)
    comment_text = models.CharField(max_length=1000)
    comment_date = models.DateTimeField(auto_now_add=True)
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()
