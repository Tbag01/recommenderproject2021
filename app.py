from flask import Flask,render_template,request
import pickle
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


df = pd.read_csv("dataset/movie_dataset.csv")

app = Flask(__name__, template_folder='templates')

@app.route('/', methods=["GET","POST"])
def main():
    if request.method == 'GET':
        return(render_template('main.html'))
    
    if request.method == 'POST':
        movie = request.form['movie']
        number = int(request.form['num'])

        count_matrix = pickle.load(open('model/Model.pkl','rb'))
        cosine_sim = cosine_similarity(count_matrix)
        def get_title_from_index(index):
            return df[df.index == index]["title"].values[0]
        def get_index_from_title(title):
            return df[df.title == title]["index"].values[0]

        movie_user_likes = str(movie)

        movie_index = get_index_from_title(movie_user_likes)
        similar_movies = list(enumerate(cosine_sim[movie_index])) #accessing the row corresponding to given movie to find all the similarity scores for that movie and then enumerating over it
        sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)[1:]
        i = number
        movie_list = []
        if len(movie_list) < number:
            number = len(movie_list)
        for element in sorted_similar_movies:
            movie_title = get_title_from_index(element[0])
            movie_list.append(movie_title)
            i=i-1
            if i==0:
                break

        return render_template('main.html',result=movie_list)

if __name__ == '__main__':
    app.run(debug=True)