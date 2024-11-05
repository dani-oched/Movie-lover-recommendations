from flask import Flask, render_template, request
from letterboxd_watchlist import getAllCommonFilms  # Import your comparison function here

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/compare', methods=['POST'])
def compare():
    # Get usernames from the form
    usernames = request.form.getlist('usernames')
    usernames = usernames[0].split(', ')
    
    # Assuming `get_common_movies` is a function that takes a list of usernames
    # and returns a list of common movies

    common_movies = getAllCommonFilms(*usernames)
    
    return render_template('index.html', common_movies=common_movies, usernames=usernames)

if __name__ == '__main__':
    app.run(debug=True)