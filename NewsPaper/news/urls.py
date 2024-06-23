from django.urls import path
from .views import PostList, PostDetail, NewsPostList, ArticlePostList, NewsSearch

urlpatterns = [
    path ('', PostList.as_view()),
    path ('<int:pk>', PostDetail.as_view()),
    path('news/', NewsPostList.as_view()),
    path('article/', ArticlePostList.as_view()),
    path('news/search/', NewsSearch.as_view()),
]