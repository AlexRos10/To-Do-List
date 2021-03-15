from airtable import *
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

base_key = 'secret_key'
table_name = 'Tasks'
airtable = Airtable(base_key, table_name, 'airtable_api_key')

def get_tasks():
    tasks = []
    for page in airtable.get_iter():
        for record in page:
            value = record['fields']['Notes']
            tasks.append(value)
            
    return tasks

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html', tasks=get_tasks())

@app.route('/index', methods = ['GET', 'POST'])
def index():
    task = request.form['task']
    airtable.insert({'Notes': task})

    return redirect('/home')

@app.route('/subtrac', methods = ['GET', 'POST'])
def subtrac():
    close = request.form['close']
    record = airtable.match('Notes', close)
    airtable.delete(record['id'])

    return redirect("/home")

if __name__ == '__main__':
    app.run(debug=True, port=2000)
