from flask import Flask, render_template, request
from letterboxd_watchlist import getAllCommonFilms, getAllPosters

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    usernames = request.form.getlist('usernames')
    usernames = usernames[0].split(', ')

    common_movies = getAllCommonFilms(*usernames)
    img_urls = getAllPosters(common_movies)
    movies = []
    for i, j in zip(common_movies, img_urls):
        movies.append({'name': i, 'image_url': j, 'link': 'https://letterboxd.com/film/'+i+'/'})
    
    return render_template('index.html', common_movies=movies, usernames=usernames)

if __name__ == '__main__':
    app.run(debug=True)