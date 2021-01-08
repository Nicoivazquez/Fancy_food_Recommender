from flask import Flask, render_template, url_for, request
import numpy as np
from sklearn.datasets import load_iris
import pickle

app = Flask(__name__)

@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    return render_template("home.html")



@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/eda')
def eda():
    column_options = [1, 2, 3, 4]
    return render_template("eda.html", column_options=column_options)

@app.route('/graphs', methods=['POST'])
def graphs():
    col1 = int(request.form['column1']) - 1
    col2 = int(request.form['column2']) - 1

    t1 = str(request.form['text_input1'])
    t2 = str(request.form['text_input2'])


    if col1 == col2:
        return f'Why do you want to graph column {col1+1} by itself?!'
    else:
        return render_template('graphs.html', col1=col1+1, col2=col2+1, url=f'./static/images/col{col1}col{col2}.png')

@app.route('/predict')
def predict():
    return render_template('predict.html')


@app.route('/results', methods=['POST'])
def results():
    sepal_length = float(request.form['sepal_length'])
    sepal_width = float(request.form['sepal_width'])
    petal_length = float(request.form['petal_length'])
    petal_width = float(request.form['petal_width'])

    test_data = np.array([sepal_length, sepal_width, petal_length, petal_width]).reshape(1, -1)

    # Load model
    filename = 'iris_log_regr.pkl'
    model = pickle.load(open(filename, 'rb'))

    # Predict on user input
    prediction = model.predict(test_data)

    # Load iris dataset to get target names
    data = load_iris()
    target_names = data.target_names

    # Index target names at prediction value
    for name in target_names[prediction]:
        predicted_name = name

    return render_template('results.html', prediction=predicted_name, image=f'./static/images/iris.png')



if __name__=="__main__":
    app.run(debug=True)


