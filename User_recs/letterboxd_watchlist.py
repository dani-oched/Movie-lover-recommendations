import requests
from bs4 import BeautifulSoup

### Obtain all films in watchlist ###

def getSoup(url):
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup

def getIntfromStr(text) -> int:
    indxs = [i for i in range(len(text)) if text[i].isdigit()]
    res = int(''.join([text[i] for i in indxs]))
    return res

class lbWatchlist():
    def __init__(self, user):
        self.user = user
        self.n_page = 28
        self.getAllFilmTitles()

    def getFilmCount(self, soup) -> int:
        film_count = soup.find(class_='js-watchlist-count').text
        return getIntfromStr(film_count)

    def getFilmTitles(self, soup) -> list():
        poster_containers = soup.find_all('li', class_='poster-container')
        titles = []
        for poster_container in poster_containers:
            title = poster_container.find("div")['data-film-slug']
            titles.append(title)
        return titles

    def getAllFilmTitles(self) -> list():
        url = f'https://letterboxd.com/{self.user}/watchlist/'
        soup = getSoup(url)
        self.film_count = self.getFilmCount(soup)
        self.page_count = self.film_count//self.n_page + 1

        titles = []
        for i in range(1, self.page_count + 1):
            new_url = url + 'page/' + str(i)
            new_soup = getSoup(new_url)
            titles += self.getFilmTitles(new_soup)

        try:
            assert len(titles) == self.film_count, 'Film number incorrect'
        except AssertionError as msg:
            print(msg)

        self.titles = titles

def getAllCommonFilms(*users):
    if not users:
        return set()
    film_lists = []
    for user in users:
        film_lists.append(lbWatchlist(user).titles)
    common_films = set(film_lists[0])
    for film_list in film_lists:
        common_films &= set(film_list)
    return list(common_films)

def getPoster(film: str):
    lb_url = f'https://letterboxd.com/film/{film}/'
    lb_soup = getSoup(lb_url)
    film_id = lb_soup.find(class_='film')['data-tmdb-id']
    tmdb_url = f'https://www.themoviedb.org/movie/{film_id}'
    tmdb_soup = getSoup(tmdb_url)
    img_src = tmdb_soup.find(class_='poster w-full')['src']
    return img_src

def getAllPosters(films: list()):
    img_srcs = []
    for film in films:
        img_srcs.append(getPoster(film))
    return img_srcs
