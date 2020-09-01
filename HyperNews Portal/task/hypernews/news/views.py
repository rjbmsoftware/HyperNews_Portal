import time
from datetime import datetime
from django.shortcuts import render, redirect, Http404
from django.views import View
from django.conf import settings
import json


class Home(View):
    def get(self, request, *args, **kwargs):
        return redirect('news/')

class NewsArticle(View):
    def get(self, request, *args, **kwargs):
        context = NewsArticle.read_json_news(kwargs['article_link_id'])
        return render(request, "news/news_article.html", context=context)

    @classmethod
    def read_json_news(cls, article_link_id) -> []:
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            json_text = json_file.read()
            articles = json.loads(json_text)
            for article in articles:
                if article['link'] == article_link_id:
                    return article
        return []


class NewsHomePage(View):
    def get(self, request, *args, **kwargs):
        if 'q' in request.GET:
            filter_for = NewsHomePage.articles_containing(request.GET.get('q'))
            articles = NewsHomePage.all_news_grouped_by_date(filter_for)
            context = {'articles': articles}
        else:
            context = {'articles': NewsHomePage.all_news_grouped_by_date(self.all_articles())}

        return render(request, "news/news_home.html", context=context)

    @classmethod
    def articles_containing(cls, title_text: str) -> {}:
        """
        searches all article titles for title text
        """
        articles = cls.all_articles()
        return [article for article in articles if title_text in article['title']]

    @classmethod
    def all_articles(cls) -> {}:
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            return json.loads(json_file.read())

    @classmethod
    def all_news_grouped_by_date(cls, articles: {}) -> {}:
        """
        gets news articles grouped by date, keys are ordered
        date desc
        """
        articles_grouped_by_date = {}
        for article in articles:
            date = article['created'][:10]
            if date in articles_grouped_by_date:
                articles_grouped_by_date[date].append(article)
            else:
                articles_grouped_by_date[date] = [article]

        return dict(sorted(articles_grouped_by_date.items(), key=lambda item: item[0], reverse=True))


class CreateNewsArticle(View):
    def get(self, request, *args, **kwargs):
        return render(request, "news/create_news_article.html")

    def post(self, request, *args, **kwargs):
        print('test')
        title = request.POST.get('title')
        text = request.POST.get('text')
        article = self.news_article(title, text)
        self.save_article(article)

        return redirect('/news/')

    @classmethod
    def news_article(cls, title: str, text: str) -> []:
        created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        link = int(round(time.time() * 1000))
        return {
            'created': created,
            'text': text,
            'title': title,
            'link': link
        }

    @classmethod
    def save_article(cls, article: []) -> None:
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            json_text = json_file.read()

        articles = json.loads(json_text)
        articles.append(article)
        output_json = json.dumps(articles)

        with open(settings.NEWS_JSON_PATH, 'w') as json_file:
            json_file.writelines(output_json)
