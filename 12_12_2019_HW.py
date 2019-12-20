import requests

from flask import Flask
from faker import Faker

app = Flask('app')


@app.route('/req')
def requirements():
    with open('requirements.txt') as f:
        return '<br>'.join(row for row in f.read().split('\n'))


@app.route('/users')
def users():
    fake = Faker()
    return '<br>'.join((fake.name() + ': ' + fake.email()) for i in range(100))


@app.route('/average')
def average():
    with open('hw.csv') as f:
        content = f.read().split('\n')[1:]

    number_of_records = 0
    height_sum = 0
    weight_sum = 0

    for row in content:
        if not row:
            continue
        number_of_records += 1
        height = float(row.split(',')[1])
        weight = float(row.split(',')[2])
        height_sum += height
        weight_sum += weight
    average_height = round(height_sum / number_of_records, 2)
    average_weight = round(weight_sum / number_of_records, 2)

    return f"Average height: {average_height} Inches; <br> Average weight: {average_weight} Pounds"


@app.route('/spaceman')
def hello():
    r = requests.get('http://api.open-notify.org/astros.json')
    spacemen_quantity = r.json()
    return f"Spaceman's quantity: {spacemen_quantity['number']}"


if __name__ == '__main__':
    app.run()