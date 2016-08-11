#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from collections import namedtuple
import requests
from article_html import ArticleHtml
from cache_link import CacheLink
from mail import Mail

BASE_URL = "http://nrc.nl"
LINK_CLASS = "nmt-item__link"
TAG_CLASS = "nmt-item__flag"
HEADLINE_CLASS = "nmt-item__headline"
TEASER_CLASS = "nmt-item__teaser"

ArticleRecord = namedtuple('ArticleRecord', 'url tag headline teaser')

cache_link = CacheLink()
article_html = ArticleHtml()

def get_html():
    resp = requests.get(BASE_URL)
    if resp.status_code != 200:
        print("Cannot get html for %s" % BASE_URL)
        sys.exit(1)
    return resp.text

def get_articles(html):
    soup = BeautifulSoup(html, "html5lib")
    return soup.find_all("a", {"class": LINK_CLASS})

def get_article_records(articles):
    for article in articles: 
        url = article['href']
        tag = article.parent.find("h6", {"class": TAG_CLASS})
        headline = article.parent.find("h3", {"class": HEADLINE_CLASS})
        teaser = article.parent.find("div", {"class": TEASER_CLASS})
        if not all([teaser, tag, headline]):
            continue
        yield ArticleRecord(url=url, tag=tag.text, headline=headline.text, teaser=teaser.text)

def _article_in_cache(url):
    return cache_link.link_in_cache(url)

def generate_html_output(articles, cache_enabled=True):
    output = []
    for art_rec in get_article_records(articles):
        if cache_enabled and _article_in_cache(art_rec.url):
            continue
        cache_link.cache_link(art_rec.url)
        output.append(article_html.create_article_html(art_rec))
    return output

def mail_output(output):
    mail = Mail()
    subject = "NRC news digest (source: nrc.nl)"
    mail.send_email(subject, "\n".join(output))    

if __name__ == "__main__":
    html = get_html()
    articles = get_articles(html)
    output = generate_html_output(articles, cache_enabled=False)
    if output:
        print("New articles, sending digest mail")
        mail_output(output)
    else:
        print("No new articles found")
