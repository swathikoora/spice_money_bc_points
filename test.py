from flask import Flask, render_template, request
import pandas as pd
import os
from data_analytics import sum_designation
from BCPoints_vscode import bcpoints
app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    # if request.method == 'POST': 
    # Check if the POST request has the file part
    vendor = request.form['vendor']
    # if 'file' not in request.files:
    #     return render_template('index.html', message='No file part')
        
    file = request.files['file']
        
    # If the user does not select a file, the browser submits an empty file without a filename
    if file.filename == '':
        return render_template('index.html', message='No selected file')
        
    if file:
        # Perform backend data analysis (Example: just reading and displaying some info)
        df = pd.read_excel(file)
        result = bcpoints(df,vendor)
        # num_rows, num_cols = df.shape
        # sum_sal = df[df['Designation']== designation]['Salary'].sum()
        html_table = result.to_html()
        return render_template('index.html', message='File uploaded successfully!', info=html_table)

if __name__ == '__main__':
    host = os.getenv('FLASK_HOST', '127.0.0.1')
    port = os.getenv('FLASK_PORT', '5000')
    app.run(debug = True)

