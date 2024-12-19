import requests
import json
from datetime import datetime
from fake_headers import Headers
from time import sleep
from tqdm import tqdm
import re
import pandas as pd
# import csv



class Scraper():

    MAINDOMAIN = 'https://www.imdb.com/'
    
    def __init__(self, browser= "chrome", os= "win"):
        self.date = datetime.now()
        self.agent = Headers(browser= browser,
                                      os= os,
                                      headers=True).generate()
        self._structure()

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
            'ids_directors' : [],
            'directors' : [],
            'ids_creators' : [],
            'creators' : [],
            'ids_actors' : [],
            'keywords' : [],
            'actors' : []
            # 'gus' : []
            }


    def extract_mainpage(self):
        response = requests.get(self.MAINDOMAIN + 'chart/top/', headers=self.agent, verify=False)
        json_str = re.search(r'<script type="application/ld\+json">(.*?)</script>', response.text, re.DOTALL).group(1)

        if response.status_code <= 200:
            print("Successfully Connected !")
            self.movies = json.loads(json_str)
            self.number = len(self.movies['itemListElement'])

        else:
            print("We have an Issue\nCheck your connection")
            print(response.text)
            exit(1)

        for i in range(self.number): #range(self.number)
            movie = self.movies['itemListElement'][i]
            self.dataframe['title'].append(movie['item']['name'])
            # print(movie['item']['name'])
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
            self.dataframe['duration'].append(movie['item']['duration'][2:])


    def extract_movie_page(self, film_id, index=None):
        self.agent =  Headers(headers=True).generate()
        response = requests.get(self.MAINDOMAIN + f'title/{film_id}/', headers=self.agent, verify=False)
        pattern = r'<script type="application/ld\+json">\s*(\{.*?\})\s*</script>'
        match = re.search(pattern, response.text, re.DOTALL)

        if match:
            json_data = match.group(1)
            parsed_data = json.loads(json_data)
        else:
            print(f"No JSON found In movie Id : {film_id}")
            return

        # Extract actors and their IDs with None handling
        actors = []
        ids_actors = []
        for actor in parsed_data.get('actor', []):
            actors.append(actor.get('name', None))
            actor_id = actor.get('url', '').split('/')[-2] if actor.get('url') else None
            ids_actors.append(actor_id)

        # Extract directors and their IDs with None handling
        directors = []
        ids_directors = []
        director_data = parsed_data.get('director', {})
        if isinstance(director_data, list):
            for director in director_data:
                directors.append(director.get('name', None))
                director_id = director.get('url', '').split('/')[-2] if director.get('url') else None
                ids_directors.append(director_id)
        elif isinstance(director_data, dict):
            directors.append(director_data.get('name', None))
            director_id = director_data.get('url', '').split('/')[-2] if director_data.get('url') else None
            ids_directors.append(director_id)

        # Extract creators and their IDs with None handling
        creators = []
        ids_creators = []
        if 'creator' in parsed_data:
            creator_data = parsed_data['creator']
            if isinstance(creator_data, list):
                for creator in creator_data:
                    if creator.get('@type') == 'Person':
                        creators.append(creator.get('name', None))
                        creator_id = creator.get('url', '').split('/')[-2] if creator.get('url') else None
                        ids_creators.append(creator_id)
            elif isinstance(creator_data, dict) and creator_data.get('@type') == 'Person':
                creators.append(creator_data.get('name', None))
                creator_id = creator_data.get('url', '').split('/')[-2] if creator_data.get('url') else None
                ids_creators.append(creator_id)

        # Append to dataframe with None handling
        self.dataframe['year'].append(parsed_data.get('datePublished', None))
        self.dataframe['keywords'].append(parsed_data.get('keywords', None))
        self.dataframe['genre'].append(parsed_data.get('genre', []))
        
        # Add actors, directors, and creators
        self.dataframe['actors'].append(actors or None)
        self.dataframe['ids_actors'].append(ids_actors or None)
        
        self.dataframe['directors'].append(directors or None)
        self.dataframe['ids_directors'].append(ids_directors or None)
        
        self.dataframe['creators'].append(creators or None)
        self.dataframe['ids_creators'].append(ids_creators or None)


        # print(f"Done with {film_id}")
        # print(self.dataframe)

    def iterating(self):

        counter = 0
        for id in tqdm(self.dataframe['movie_id'], desc="Extracting Movie Pages", colour="GREEN"):
            if id is not None:
                self.extract_movie_page(id)
                sleep(.65)
            else:
                continue

            if counter in [70, 145, 210]:
                sleep(10)

            # counter += 1
            # For testing purposes
            # if counter >= 5:
            #     break
            counter += 1

    def save_file(self):

        # for key, value in self.dataframe.items():
        #     print(f"{key}: {len(value)}")
            
        # Save JSON file
        with open(f'ExtractedData/{self.date.date()}_IMDB{self.number}.json', 'w', encoding='utf-8') as f:
            json.dump(self.dataframe, f, ensure_ascii=False, indent=4)


        df = pd.DataFrame(self.dataframe)
        df.to_csv(f'ExtractedData/{self.date.date()}_IMDB{self.number}.csv', index=False, encoding='utf-8')

        print("Scraping Completed!")
        print(f"Saved {self.date.date()}_IMDB{self.number}.csv")
        # Save CSV file
        # with open(f'ExtractedData/{self.date.date()}_IMDB{self.number}.csv', 'w', newline='', encoding='utf-8') as f:
        #     writer = csv.writer(f)
            
        #     # Write headers
        #     writer.writerow(self.dataframe.keys())
            
        #     # Transpose the data to write rows correctly
        #     max_length = max(len(lst) for lst in self.dataframe.values())
            
        #     # Pad lists to ensure equal length
        #     for key in self.dataframe:
        #         if len(self.dataframe[key]) < max_length:
        #             self.dataframe[key].extend([None] * (max_length - len(self.dataframe[key])))
            
        #     # Write rows
        #     rows = list(zip(*self.dataframe.values()))
        #     writer.writerows(rows)

    
