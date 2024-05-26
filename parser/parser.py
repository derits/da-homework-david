import requests
from bs4 import BeautifulSoup


class Article:
    def __init__(self, title: str, description: str, url: str, imgUrl: str, time: str, date: str):
        self.title = title
        self.description = description
        self.url = url
        self.imgUrl = imgUrl
        self.time = time
        self.date = date

    def __repr__(self) -> str:
        return "=====\n{}\n{}\n{}\n{}\n{}\n{}\n======\n".format(self.title, self.description, self.url, self.imgUrl,
                                                                self.time, self.date)


class NewsArmeniaParser(object):
    baseUrl: str = "https://newsarmenia.am"
    url: str = "https://newsarmenia.am/news/armenia/?PAGEN_3="
    pageCount: int

    def __init__(self, pageCount: int):
        if pageCount < 1:
            raise ValueError("Количество страниц не может быть меньше 1")
        self.pageCount = pageCount

    def parse_page(self, number: int) -> list[Article]:
        url = self.url + str(number)
        print("Parsing page #" + str(number) + ": " + url)
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        news = soup.findAll("div", class_="markerListerItem")

        articles: list[Article] = []

        for post in news:
            title = post.find("a", "markerListerItem-title").getText()
            description = post.find("div", "markerListerItem-desc").getText()
            postUrl = self.baseUrl + post.find("a", "markerListerItem-title")['href']
            imgUrl = self.baseUrl + post.find("img", "img-responsive")['src']
            time = post.find("div", "markerListerItem-time").getText()
            date = post.find("div", "markerListerItem-date").getText()

            articles.append(Article(title, description, postUrl, imgUrl, time, date))

        return articles

    def parse(self) -> list[Article]:
        startPage = 1

        articles: list[Article] = []
        for x in range(startPage, self.pageCount + 1):
            articles.extend(self.parse_page(x))

        return articles
