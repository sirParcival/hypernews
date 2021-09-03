import json
import os
import uuid
from django.http import JsonResponse
import hypernews.settings as settings
from django.shortcuts import render, HttpResponse, redirect
from django import views
from datetime import datetime


# Create your views here.

class Home(views.View):
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return redirect('news')


class NewsDetail(views.View):
    @staticmethod
    def get_data():
        with open(settings.NEWS_JSON_PATH, 'r') as file:
            data = json.loads(file.read())
        return data

    template_name = "news_detail.html"

    def get(self, request, *args, **kwargs):
        article = self.get_article(kwargs['link'])
        context={'article': article}
        return render(request, self.template_name, context=context)

    def get_article(self, identifier):
        for article in self.get_data():
            if article['link'] == identifier:
                return article
        return None


class News(views.View):
    template_name = "news.html"

    def get(self, request, *args, **kwargs):

        data = sorted(NewsDetail.get_data(), key=lambda k: datetime.strptime(k['created'], "%Y-%m-%d %H:%M:%S"))
        for element in data:
            element['created'] = element['created'][:10]
        search = request.GET.get('q', None)
        if search:
            data, tmp_data = [], data
            for article in tmp_data:
                if article['title'].lower() == search.lower() or search.lower() in article['title'].lower():
                    data.append(article)
        context = {'articles': reversed(data)}

        return render(request, self.template_name, context=context)


class CreateArticle(views.View):
    template_name = "news_creator.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        data = NewsDetail.get_data()
        new_article = {"title": request.POST['title'], "text": request.POST['text']}
        timestamp = f"{datetime.now().date()} {datetime.now().time().isoformat(timespec='seconds')}"
        link = int(uuid.uuid4())
        new_article['created'] = timestamp
        new_article['link'] = link
        data.append(new_article)
        with open(settings.NEWS_JSON_PATH, 'w') as file:
            file.write(json.dumps(data))
        return redirect('news')
