import requests
import json
from datetime import datetime
from fake_headers import Headers
import re


class Scraper():

    MAINDOMAIN = 'https://www.imdb.com/'

    def __init__(self, browser= "chrome", os= "win"):
        self.date = datetime.now()
        self.agent = Headers(browser= browser,
                                      os= os,
                                      headers=True).generate()

    def _structure(self):
        self.dataframe = {
            'movie_id' : [],
            'title' : [],
            'rating': [],
            'No.rates': [],
            'description': [],
            'year' : [],
            'parental' : [],
            'duration' : [],
            'genre' : [],
            'id_director' : [],
            'director' : [],
            'ids_writer' : [],
            'writers' : [],
            'ids_stars' : [],
            'stars' : [],
            'gus' : []
            }

    def base_info(self):
        response = requests.get(self.MAINDOMAIN + 'chart/top/', headers=self.agent)
        json_str = re.search(r'<script type="application/ld\+json">(.*?)</script>', response.text, re.DOTALL).group(1)

        if response.status_code <= 200:
            print("Successfully Connected !")
            self._structure()
            self.movies = json.loads(json_str)
            self.number = len(self.movies['itemListElement'])


            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(self.movies, f, ensure_ascii=False, indent=4)

        else:
            print("We have an Issue\nCheck your connection")
            print(response.text)
            exit(1)

    def extract_mainpage(self):

        for i in range(self.number):
            movie = self.movies['itemListElement'][i]
            self.dataframe['title'].append(movie['item']['name'])
            print(movie['item']['name'])
            self.dataframe['rating'].append(float(movie['item']['aggregateRating']['ratingValue']))
            self.dataframe['No.rates'].append(int(movie['item']['aggregateRating']['ratingCount']))
            try:
                self.dataframe['movie_id'].append(str(movie['item']['url']).split('/')[4])
            except Exception as e:
                self.dataframe['movie_id'].append(None)
            self.dataframe['description'].append(movie['item']['description'])
            try:
                self.dataframe['parental'].append(movie['item']['contentRating'])
            except Exception as e:
                self.dataframe['parental'].append(None)
            self.dataframe['genre'].append(movie['item']['genre'])
            self.dataframe['duration'].append(movie['item']['duration'][2:])

    def extract_moviepage(self, film_id, index=None):

        response = requests.get(self.MAINDOMAIN + f'title/{film_id}/', headers=self.agent)
        # Regex pattern to extract the JSON content
        pattern = r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>'

        # Find the JSON in the HTML
        match = re.search(pattern, response.text, re.DOTALL)

        if match:
            json_data = match.group(1)
            # Parse the JSON string
            parsed_data = json.loads(json_data)
            print(parsed_data)
        else:
            print(f"No JSON found In movie Id : {film_id}")

