from django.urls import path
from .views import Home, NewsDetail, News, CreateArticle

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('news/<int:link>/', NewsDetail.as_view()),
    path('news/', News.as_view(), name='news'),
    path('news/create/', CreateArticle.as_view())
]
