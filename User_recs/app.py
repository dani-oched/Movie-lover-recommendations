from flask import Flask, render_template, request
from letterboxd_watchlist import getAllCommonFilms, getAllPosters

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    # usernames = request.form.getlist('usernames')
    # usernames = usernames[0].split(', ')
    user1 = request.form.getlist('user1')[0]
    user2 = request.form.getlist('user2')[0]

    common_movies = getAllCommonFilms(user1, user2)
    img_urls = getAllPosters(common_movies)
    movies = []
    for i, j in zip(common_movies, img_urls):
        movies.append({'name': i, 'image_url': j, 'link': 'https://letterboxd.com/film/'+i+'/'})
    
    return render_template('index.html', common_movies=movies, usernames=[user1, user2])

if __name__ == '__main__':
    app.run(debug=True)