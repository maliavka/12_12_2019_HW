import requests
import random
import string

from flask import Flask
from flask import request
from faker import Faker

from data_base import exec_query

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


@app.route('/gen_len')
def gen_len():
    length = request.args["len"]
    if length.isdigit() and 1 <= len(length) <= 100:
        return ''.join(random.choice(string.ascii_uppercase) for i in range(int(length)))
    else:
        return 'Error: string length is not valid'


@app.route('/all-customers')
def all_customers():
    state = request.args["State"]
    country = request.args["Country"]
    query = f'SELECT * FROM Customers WHERE State = \'{state}\' AND Country = \'{country}\';'
    result = exec_query(query)
    return str(result)


@app.route('/names')
def names():
    query = f'SELECT FirstName FROM Customers;'
    result = str(exec_query(query))
    list_names = []
    for i in result.split():
        if i in list_names:
            continue
        else:
            list_names.append(i)
    return f' Number of different names: {str(len(list_names))}'


@app.route('/profit')
def total_profit():
    query = f'SELECT UnitPrice, Quantity FROM invoice_items;'
    result = str(exec_query(query)).replace('), (', ') (')
    result = result.replace(', ', ',')
    result = result.replace('[', '')
    result = result.replace(']', '')
    result = result.replace('(', '')
    result = result.replace(')', '')
    profit = 0
    for i in result.split():
        i = i.split(',')
        profit = float(i[0]) * int(i[1]) + profit

    return f'Total profit: {str(round(profit, 2))}'


if __name__ == '__main__':
    app.run()
