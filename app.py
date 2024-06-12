from flask import Flask
from flask import render_template
from analysis import getNeg, getNeu, getPos
from hashtagAnalysis import getHashTags
from location_analysis import getLoc, getCount
from flask import request

app = Flask(__name__ ,template_folder='venv/templates')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/sentiment')
def sentiment():
    num_positive = getPos()
    num_negative = getNeg()
    num_neutral = getNeu()
    return render_template('sentiment.html', num_positive=num_positive, num_negative=num_negative, num_neutral=num_neutral)

@app.route('/hashtags')
def hashtag():
    hashtags = getHashTags()
    table = hashtags.to_html(index=False, classes='table table-striped')
    return render_template('hashtags.html', table=table)

@app.route('/location', methods =["GET", "POST"])
def location():
    labels = getLoc()
    values = getCount()

    # if request.method == "POST":
    #     location_name = request.form.get("lname")
    #     count = getCountNew(location_name.lower())
    #     labels.append(location_name)
    #     values.append(count)
    return render_template('location.html', values=values, labels=labels)  

if __name__ == '__main__':
    app.run(debug=True)
