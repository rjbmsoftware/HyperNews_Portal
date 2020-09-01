from django.urls import path
from .views import NewsArticle, NewsHomePage, CreateNewsArticle, Home

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('news/<int:article_link_id>/', NewsArticle.as_view(), name='news_article'),
    path('news/', NewsHomePage.as_view(), name='news_home'),
    path('news/create/', CreateNewsArticle.as_view(), name='news_create')
]
