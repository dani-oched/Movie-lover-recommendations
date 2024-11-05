from flask import Flask, render_template, request
from letterboxd_watchlist import getAllCommonFilms

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    usernames = request.form.getlist('usernames')
    usernames = usernames[0].split(', ')

    common_movies = getAllCommonFilms(*usernames)
    
    return render_template('index.html', common_movies=common_movies, usernames=usernames)

if __name__ == '__main__':
    app.run(debug=True)