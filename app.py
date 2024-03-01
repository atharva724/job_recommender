from flask import Flask, render_template, request
import pandas as pd
import numpy as np

jobs = pd.read_pickle(open('jobs.pkl', 'rb'))
similarity1 = pd.read_pickle(open('similarity1.pkl', 'rb'))
similarity2 = pd.read_pickle(open('similarity2.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search')
def search_ui():
    return render_template('search.html', search_results=None)

@app.route('/recommend', methods = ['post'])
def recommend():
    user_input = request.form['user_input'].lower()

    if user_input not in jobs['Post'].values \
            and user_input not in jobs['Location'].values \
            and user_input not in jobs['Job_Domain'].values:
        error_message = "Entered value not found in the dataset."
        return render_template('search.html', error_message=error_message)
    elif user_input in jobs['Post'].values:
        index = np.where(jobs['Post'] == user_input)[0][0]
        similar_jobs = sorted(list(enumerate(similarity1[index])), key=lambda x: x[1], reverse=True)[1:10]
    elif user_input in jobs['Location'].values:
        index = np.where(jobs['Location'] == user_input)[0][0]
        similar_jobs = sorted(list(enumerate(similarity2[index])), key=lambda x: x[1], reverse=True)[1:10]
    else:
        index = np.where(jobs['Job_Domain'] == user_input)[0][0]
        similar_jobs = sorted(list(enumerate(similarity1[index])), key=lambda x: x[1], reverse=True)[1:10]

    search_results = []
    for i in similar_jobs:
        job = jobs.iloc[i[0]]
        search_results.append({'Company': job['Company'], 'Post': job['Post'], 'Location': job['Location'], 'Job_Domain': job['Job_Domain'],
                               'Salary': job['Salary']})

    return render_template('search.html', search_results=search_results)



if __name__ == '__main__':
    app.run(debug = True)
