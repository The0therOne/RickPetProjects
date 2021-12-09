import requests
from bs4 import BeautifulSoup
import webbrowser

#  https://en.wikipedia.org/wiki/Special:Random
#  link to random pages on wiki EN

#  https://ru.wikipedia.org/wiki/Специальная:Случайная_Страница
#  (link to random pages on wiki RU...but you need to encode url)

#  https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0

random_article_url_rand_en = "https://en.wikipedia.org/wiki/Special:Random"
random_article_url_rand_ru = "https://ru.wikipedia.org/wiki/%D0%A1%D0%BB%D1%83%D0%B6%D0%B5%D0%B1%D0%BD%D0%B0%D1%8F:%D0%A1%D0%BB%D1%83%D1%87%D0%B0%D0%B9%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"


def get_random_article(lan='en'):
    if lan == 'en':
        random_article_url_response = requests.get(random_article_url_rand_en)
        random_article_url = random_article_url_response.url
        soup = BeautifulSoup(random_article_url_response.content, "html.parser")
        title = soup.find('title')
        new_title = str(title).replace('b', '').replace('<title>', '').replace('</title>', '')
        return new_title, random_article_url
    elif lan == 'ru':
        random_article_url_response = requests.get(random_article_url_rand_ru)
        random_article_url = random_article_url_response.url
        soup = BeautifulSoup(random_article_url_response.content, "html.parser")
        title = soup.find('title')
        new_title = str(title).replace('b', '').replace('<title>', '').replace('</title>', '')
        return new_title, random_article_url


print("Hello! Welcome to my random wiki reader.")
lan_choice = input("Choose your language ('ru' or 'en') : ")
while lan_choice not in ('ru', 'en'):
    print('Wrong input! Please choose ru or en!')
    lan_choice = input("Choose your language ('ru' or 'en') : ")
answer = ''
article, article_url = get_random_article(lan_choice)
while answer != 'exit':
    answer = input(f"Do you want read about '{article}' ? (y/n/exit)\n").lower()
    if answer == 'y':
        webbrowser.open(article_url, new=2)
        article, article_url = get_random_article(lan_choice)
    elif answer == 'n':
        article, article_url = get_random_article(lan_choice)
    elif answer not in ('y', 'n', 'exit'):
        print('Wrong input! Please choose (y/n/exit)!')
        continue
print('Bye bye, reader!')
