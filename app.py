from flask import Flask, render_template
from mysql.connector import connect
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
import re

app = Flask(__name__)

#update bagian ini jika berbeda dengan yang biasanya digunakan
mysqlConnection = connect(
    host='localhost',
    port=3306,
    user='root',
    password='',
    database='imdb_scrapping'
)

def update_movie(id, title, rating):
    cursor = mysqlConnection.cursor()
    try:
        cursor.execute(f'UPDATE `movies` SET `title`="{title}", `rating`="{rating}" WHERE `id`={id}')
        mysqlConnection.commit()
    except Exception as err:
        mysqlConnection.rollback()
        print(err)
    finally:
        cursor.close()

def movie_exists(title, rating):
    cursor = mysqlConnection.cursor()
    try:
        cursor.execute(f'SELECT * FROM `movies` WHERE `title`="{title}" AND `rating`="{rating}"')
        result = cursor.fetchone()
        return result is not None
    except Exception as err:
        print(err)
    finally:
        cursor.close()

def insert_movie(title, rating):
    cursor = mysqlConnection.cursor()
    try:
        cursor.execute(f'INSERT INTO `movies` (`title`, `rating`) VALUES ("{title}", "{rating}")')
        mysqlConnection.commit()
    except Exception as err:
        mysqlConnection.rollback()
        print(err)
    finally:
        cursor.close()

def get_imdb_top_movies():
    url = 'https://www.imdb.com/chart/top'
    chrome_service = ChromeService(executable_path='./chromedriver/chromedriver.exe')
    driver = webdriver.Chrome(service=chrome_service)
    driver.get(url)
    driver.implicitly_wait(10)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    movies = []

    for id, movie in enumerate(soup.select('li.ipc-metadata-list-summary-item'), start=1):
        title_elem = movie.find('h3')
        rate_elem = movie.select_one('div span.ipc-rating-star')

        if title_elem and rate_elem:
            title = title_elem.text
            rating_text = rate_elem.text if rate_elem else "N/A"

            rating = re.search(r'(\d+\.\d+)', rating_text)
            rating = rating.group(1) if rating else "N/A"
            
            movies.append({'title': title, 'rating': rating})

            if movie_exists(title, rating):
                update_movie(id, title, rating)
            else:
                insert_movie(title, rating)

    driver.quit()

    return movies

@app.route('/top_movies', methods=['GET'])
def get_top_movies():
    movies = get_imdb_top_movies()
    return render_template('index.html', top_movies=movies)

if __name__ == '__main__':
    app.run(debug=True)
