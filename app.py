import json 
from flask import Flask, jsonify, render_template, request, redirect, url_for

from models import Incomes, Expenses, ExpensesCategories

app = Flask(__name__)

expense_categories = {
    '1': ExpensesCategories('1', 'Housing'),
    '2': ExpensesCategories('2', 'Transportation'),
    '3': ExpensesCategories('3', 'Food and Groceries'),
    '4': ExpensesCategories('4', 'Utilities and Services'),
    '6': ExpensesCategories('5', 'Personal Care'),
    '7': ExpensesCategories('6', 'Entertainment and Leisure')
}

incomes_data = {}
with open('static/incomes_data.json', 'w') as json_file:
    json.dump(incomes_data, json_file)

expenses_data = {}

with open('static/expenses_data.json', 'w') as json_file:
    json.dump(expenses_data, json_file)

@app.route('/')
def home():
    return render_template('home.html', incomes=incomes_data, expenses=expenses_data)

@app.route('/incomes')
def incomes():
    return render_template('incomes.html', incomes=incomes_data)

@app.route('/expenses')
def expenses():
    with open('static/expenses_data.json', 'r') as json_file:
        expenses = json.load(json_file)
        
    return render_template('expenses.html', types=expense_categories, expenses=expenses)

@app.route('/incomes', methods=['POST'])
def add_income():
    amount = request.form['amount']
    date = request.form['date']
    category = request.form['category']
    
    ##Validation
    errors = []
    if not amount:
        errors.append('The amount must be filled.')
    if not isinstance(amount, int) and isinstance(amount, float):
        errors.append('The amount must be a number')
    if not date:
        errors.append('The date must be filled.')
    if not category:
        errors.append('The type must be filled.')
    if errors:
        return render_template('incomes.html', errors=errors, request=request, incomes=incomes_data)
    
    new_id = len(incomes_data) + 1
    incomes_data[new_id] = Incomes(new_id, amount, date, category).__dict__
    with open('static/incomes_data.json', 'w') as json_file:
        json.dump(incomes_data, json_file)
    
    return redirect(url_for('incomes'))

@app.route('/expenses', methods=['POST'])
def add_expense():
    
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']
    msg = request.form['msg']
    
    ##Validation
    errors = []
    if not amount:
        errors.append('The amount must be filled.')
    if not isinstance(amount, int) and isinstance(amount, float):
        errors.append('The amount must be a number')
    if not category:
        errors.append('The category must be filled.')
    if not date:
        errors.append('The date must be filled.')
    if not msg:
        errors.append('The msg must be filled.')
    if errors:
        return render_template('expenses.html', errors=errors, request=request, types=expense_categories, expenses=expenses_data)
    
    new_id = len(expenses_data) + 1
    expenses_data[new_id] = Expenses(new_id, amount, category, date, msg).__dict__
    
    with open('static/expenses_data.json', 'w') as json_file:
        json.dump(expenses_data, json_file)
    
    return redirect(url_for('expenses'))
    
if __name__ == '__main__':
    app.run(debug=True, port=8080)