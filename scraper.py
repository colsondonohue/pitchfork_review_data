
import scraperwiki
import lxml.html
import urllib2
import time
import random

def parse(url, modifier, page=''):
    html = scraperwiki.scrape(url + modifier + page, user_agent='Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7')
    page = lxml.html.fromstring(html)
    return page


def scrape_review(url, href):
    page = parse(url, href)
    url = url + href
    album = page.cssselect('h1.review-title')[0].text_content()

    artists_el = page.cssselect('ul.artist-list.artist-links li a')
    artists = ''
    for artist in artists_el:
        artists += artist.text_content() + ' '

    score = page.cssselect('span.score')[0].text_content()
    date = page.cssselect('span.pub-date')[0].get('title')
    reviewer = page.cssselect('a.display-name')[0].text_content()

    genres_el = page.cssselect('ul.genre-list li a')
    genres = ''
    for genre in genres_el:
        genres += genre.text_content() + ' '

    unique_keys = ['url']
    data = {
            'url': url,
            'album': album,
            'artists': artists,
            'score': score,
            'date': date,
            'reviewer': reviewer,
            'genres': genres
            }

    scraperwiki.sqlite.save(unique_keys, data)


def scrape_page(url, page):
    page = parse(url, '/reviews/albums/?page=', page)
    links = page.cssselect('a.album-link')
    for link in links:
        href = link.get('href')
        scrape_review(url, href)
        time.sleep(random.random() * 2)


def run_scraper(url, page):
    while True:
        try:
            scrape_page(url, str(page))
        except urllib2.HTTPError, e:
            if e.code == 404:
                break
            run_scraper(url, page)
        time.sleep(random.random() * 2)
        current_page += 1


base_url = 'http://pitchfork.com'
current_page = 1

run_scraper(base_url, current_page)
