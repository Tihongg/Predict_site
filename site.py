from flask import Flask, render_template, request
import pickle
import os

app = Flask(__name__)

# Загрузка модели
MODEL_PATH = "model.sav"
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Файл модели '{MODEL_PATH}' не найден.")

with open(MODEL_PATH, 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    year = request.form.get('year')
    try:
        year = int(year)
        prediction = model.predict([[year]])
        if prediction[0][0] < 0:
            prediction = [[0]]
        formatted_predict = "{:,}".format(round(prediction[0][0])).replace(",", " ")
        return render_template('index.html', prediction=formatted_predict, year=year)
    except ValueError:
        return render_template('index.html', error="Введите корректный год.")

if __name__ == '__main__':
    app.run(debug=True)