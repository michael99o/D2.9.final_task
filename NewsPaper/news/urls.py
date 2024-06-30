from django.urls import path
from .views import PostList, PostDetail, NewsPostList, ArticlePostList, NewsSearch, NewsCreate, ArticlesCreate, PostUpdate, PostDelete

urlpatterns = [
    path ('', PostList.as_view(), name = 'post_list'),
    path ('<int:pk>', PostDetail.as_view(), name = 'post_deatail'),
    path('news/', NewsPostList.as_view()),
    path('articles/', ArticlePostList.as_view()),
    path('search/', NewsSearch.as_view(), name = 'post_search'),
    path('news/create/', NewsCreate.as_view(), name = 'news_create'),
    path('articles/create/', ArticlesCreate.as_view(), name = 'articles_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name = 'post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name = 'post_delete')
]