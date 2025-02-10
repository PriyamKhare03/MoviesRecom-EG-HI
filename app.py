#from flask import Flask, render_template, request
#import pickle
#import joblib
#from joblib import load

# Initialize Flask app
app = Flask(__name__)

# Load the pickle file containing the precomputed data

english_similarity = load('English_similarity.pkl')
# Load the Hindi similarity matrix
hindi_similarity = joblib.load('hindi_similarity.pkl')
# Load the English movies DataFrame
movies_e = joblib.load('movies_E.pkl')
# Load the Hindi movies DataFrame
movies_h = joblib.load('movies_H.pkl')




# Recommend movie function (you can modify it as per your logic)
def recommend_movie(movie_name, language='English'):
    if language == 'English':
        if movie_name not in movies_e['title'].values:
            return f"Movie '{movie_name}' not found in English movies."
        
        movie_index = movies_e[movies_e['title'] == movie_name].index[0]
        distances = english_similarity[movie_index]
        recommended_movies = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
        
        return [movies_e.iloc[i[0]].title for i in recommended_movies]

    elif language == 'Hindi':
        if movie_name not in movies_h['title'].values:
            return f"Movie '{movie_name}' not found in Hindi movies."
        
        movie_index = movies_h[movies_h['title'] == movie_name].index[0]
        distances = hindi_similarity[movie_index]
        recommended_movies = sorted(list(enumerate(distances)), key=lambda x: x[1], reverse=True)[1:6]
        
        return [movies_h.iloc[i[0]].title for i in recommended_movies]
    else:
        return "Invalid language. Please choose either 'english' or 'hindi'."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        language = request.form['language']
        recommendations = recommend_movie(movie_name, language)
        
        return render_template('index.html', recommendations=recommendations, movie_name=movie_name, language=language)
    
    return render_template('index.html', recommendations=None)

if __name__ == '__main__':
    app.run(debug=True)
