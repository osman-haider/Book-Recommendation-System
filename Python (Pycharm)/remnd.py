from flask import Flask,render_template,request
import pickle
import numpy as np


papular_df = pickle.load(open('papular.pkl','rb'))
pt = pickle.load(open('pt.pkl','rb'))
book = pickle.load(open('book.pkl','rb'))
similarity_score = pickle.load(open('samescr.pkl' ,'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html",
                           book_name = list(papular_df['Book-Title'].values),
                           author = list(papular_df['Book-Author'].values),
                           image = list(papular_df['Image-URL-M'].values),
                           votes = list(papular_df['num-rating'].values),
                           rating = list(papular_df['avg-rating'].values)
                            )
@app.route('/recommend')
def recmnd_ui():
    return render_template('recommend.html')

@app.route('/recommend_books',methods=['post'])
def recommend():
    user = request.form.get('user_text')
    # first we fetch index with book name
    index = np.where(pt.index == user)[0][0]
    # now find similar items
    similar_items = sorted(list(enumerate(similarity_score[index])), key=lambda x: x[1], reverse=True)[1:6]
    data = []
    for i in similar_items:
        item = []
        temp_df = book[book['Book-Title'] == pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template('recommend.html',data=data)

if __name__ == '__main__':
    app.run(debug=True)