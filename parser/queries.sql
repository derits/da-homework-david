--  Получение новостей в заголовке которых содержится нужное слово
select articles.title, articles.url, dates.date from dates
                                 join articles on dates.id = articles.date_id
                                 where articles.title like '%Пашинян%' and
                                 dates.date >= '01.05.2024' and dates.date <= '25.05.2024';

--  Получение новостей в заголовке которых содержится нужное слово (по дням)
select count(*) as Total, dates.date
from articles
join dates on articles.date_id = dates.id
WHERE dates.date >= '01.05.2024' AND dates.date <= '20.05.2024'
AND articles.title LIKE '%Пашинян%'
group by dates.date

