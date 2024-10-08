import json 
import re
from flask import Flask, jsonify, render_template, request, redirect, url_for

from datetime import datetime

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
    """Render the home page"""
    return render_template('home.html', incomes=incomes_data, expenses=expenses_data)

@app.route('/incomes')
def incomes():
    """Render the incomes page"""
    with open('static/incomes_data.json', 'r') as file:
        incomes = json.load(file)
    return render_template('incomes.html', incomes=incomes)

@app.route('/expenses')
def expenses():
    """Render the expenses page"""
    with open('static/expenses_data.json', 'r') as json_file:
        expenses = json.load(json_file)
        
    return render_template('expenses.html', types=expense_categories, expenses=expenses)

@app.route('/incomes', methods=['POST'])
def add_income():
    """Add income to the json file incomes_data.json and redirect to the incomes page"""
    amount = request.form['amount']
    date = request.form['date']
    category = request.form['category']
    
    ##Validation
    errors = []
    if not re.match("^\d+\.?\d*$", amount):
        errors.append('The amount must be a number')
    if not date:
        errors.append('The date must be filled.')
    if not category:
        errors.append('The type must be filled.')
    if errors:
        return render_template('incomes.html', errors=errors, request=request, incomes=incomes_data)
    
    date = datetime.strptime(date, "%Y-%m-%d")
    formatted_date = date.strftime("%d/%m/%Y")
    new_id = len(incomes_data) + 1
    incomes_data[new_id] = Incomes(new_id, amount, formatted_date, category).__dict__
    with open('static/incomes_data.json', 'w') as json_file:
        json.dump(incomes_data, json_file)
    
    return redirect(url_for('incomes'))

@app.route('/expenses', methods=['POST'])
def add_expense():
    """Add expense to the json file expenses_data.json and redirect to the expenses page"""
    amount = request.form['amount']
    category = request.form['category']
    date = request.form['date']
    msg = request.form['msg']
    
    ##Validation
    errors = []
    if not re.match("^\d+\.?\d*$", amount):
        errors.append('The amount must be a number')
    if not category:
        errors.append('The category must be filled.')
    if not date:
        errors.append('The date must be filled.')
    if not msg:
        errors.append('The msg must be filled.')
    if errors:
        return render_template('expenses.html', errors=errors, request=request, types=expense_categories, expenses=expenses_data)
    date = datetime.strptime(date, "%Y-%m-%d")
    formatted_date = date.strftime("%d/%m/%Y")
    
    new_id = len(expenses_data) + 1
    expenses_data[new_id] = Expenses(new_id, amount, category, formatted_date, msg).__dict__
    
    with open('static/expenses_data.json', 'w') as json_file:
        json.dump(expenses_data, json_file)
    
    return redirect(url_for('expenses'))
    
@app.route('/delete_income/<id>', methods=['POST'])
def delete_income(id):
    """Delete income"""
    with open('static/incomes_data.json', 'r') as file:
        data = json.load(file)
        del data[id]
    incomes_data.clear()
    with open('static/incomes_data.json', 'w') as file:
        json.dump(data, file)
        
    return redirect(url_for('incomes'))

@app.route('/delete_expenses/<id>', methods=['POST'])
def delete_expenses(id):
    """Delete expenses"""
    with open('static/expenses_data.json', 'r') as file:
        data = json.load(file)
        del data[id]
    expenses_data.clear()
    with open('static/expenses_data.json', 'w') as file:
        json.dump(data, file)
        
    return redirect(url_for('expenses'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=4000)