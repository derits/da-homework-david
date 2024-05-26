import sqlite3
import pandas as pd
from parser import Article

DB_NAME: str = 'data.db'


def get_like_with_date(word: str, start_date: str, end_date: str) -> pd.DataFrame:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
   select articles.title,articles.url,dates.date from dates
                                 join articles on dates.id = articles.date_id
                                 where (dates.date >= ? and dates.date <= ?)
                                 and (articles.title like ?)
    """, (start_date, end_date, '%' + word + '%'))

    result = cursor.fetchall()
    connection.close()

    return pd.DataFrame(result)


def get_like_daily(word: str, start_date: str, end_date: str) -> pd.DataFrame:
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        select count(*) as Total, dates.date
        from articles
        join dates on articles.date_id = dates.id
        WHERE dates.date >= ? AND dates.date <= ?
        AND articles.title LIKE ?
        group by dates.date
    """, (start_date, end_date, '%' + word + '%'))

    result = cursor.fetchall()
    connection.close()
    return pd.DataFrame(result)



def upload_articles(articles: list[Article]):
    print("Загружаем статьи в базу данных...")
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()
    date_ids = {}
    time_ids = {}

    for article in articles:
        # Проверяем существование даты и времени в соответствующих словарях
        if article.date not in date_ids:
            cursor.execute('INSERT OR IGNORE INTO dates (date) VALUES (?)', (article.date,))
            date_ids[article.date] = cursor.lastrowid
        if article.time not in time_ids:
            cursor.execute('INSERT OR IGNORE INTO times (time) VALUES (?)', (article.time,))
            time_ids[article.time] = cursor.lastrowid

    # Вставляем статьи с корректными значениями date_id и time_id
    # IGNORE - для избежания вставки одинаковых статей (при повторном запуске программы)
    for article in articles:
        cursor.execute('''
        INSERT OR IGNORE INTO articles (title, url, img, time_id, date_id)
        VALUES (?, ?, ?, ?, ?)
        ''', (article.title, article.url, article.imgUrl, time_ids[article.time], date_ids[article.date]))

    connection.commit()
    connection.close()

    return



def create_tables():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    # create articles table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS articles(
    id INTEGER PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    url VARCHAR(255) NOT NULL UNIQUE,
    img VARCHAR(255) NOT NULL,
    time_id INTEGER NOT NULL,
    date_id INTEGER NOT NULL,
    FOREIGN KEY(date_id) REFERENCES date_id(id),
    FOREIGN KEY(time_id) REFERENCES time_id(id)
    )
    ''')

    # create dates table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS dates(
    id INTEGER PRIMARY KEY,
    date DATE UNIQUE)
    ''')

    # create times table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS times(
    id INTEGER PRIMARY KEY,
    time TIME UNIQUE)
    ''')

    connection.commit()
    connection.close()
    print('Таблицы созданы!')
