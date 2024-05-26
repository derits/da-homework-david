import pandas as pd

from parser import NewsArmeniaParser, Article
from db import create_tables, upload_articles, get_like_with_date, get_like_daily


def main():
    create_tables()
    parser = NewsArmeniaParser(int(input("Введите кол-во страниц для парсинга (минимум 1): ")))
    articles: list[Article] = parser.parse()
    upload_articles(articles)

    word = input("Введите ключевое слово для поиска: ")
    start_date = input("Введите начальную дату (дд.мм.гггг): ")
    end_date = input("Введите последнюю дату (дд.мм.гггг): ")

    articles: pd.DataFrame = get_like_with_date(word, start_date, end_date)
    print("===============================================================================")
    print("Все новости, в заголовке которых фигурирует слово " + word + " в период с " + start_date + " по " + end_date)
    print(pd.DataFrame(articles))
    print("===============================================================================")

    articles: pd.DataFrame = get_like_daily(word, start_date, end_date)
    print("===============================================================================")
    print("Все новости(по дням) содержащие слово " + word + " в период с " + start_date + " по " + end_date)
    print(pd.DataFrame(articles))
    print("===============================================================================")


if __name__ == "__main__":
    main()
