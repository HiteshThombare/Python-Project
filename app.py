from flask import Flask, render_template, request, url_for, redirect
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Load and preprocess dataset
try:
    df = pd.read_csv('Diwali Sales Data.csv', encoding='unicode_escape')
    df.drop(['Status', 'unnamed1'], axis=1, errors='ignore', inplace=True)
    df.dropna(inplace=True)
    df['Amount'] = df['Amount'].astype(int)
except FileNotFoundError:
    df = pd.DataFrame(columns=['Gender', 'Age Group', 'Marital_Status', 'State', 'Occupation', 'Product_Category', 'Amount'])


# Remove old images on startup
image_folder = "static/images"
if not os.path.exists(image_folder):
    os.makedirs(image_folder)
else:
    for filename in os.listdir(image_folder):
        file_path = os.path.join(image_folder, filename)
        if os.path.isfile(file_path):
            os.unlink(file_path)


# Helper function to generate and save plots
def generate_plot(column_name):
    plt.figure(figsize=(10, 6))
    plt.style.use('seaborn-v0_8-whitegrid')

    if column_name in df.columns:
        df.groupby(column_name)['Amount'].sum().plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title(f'Total Amount by {column_name}', fontsize=16)
        plt.xlabel(column_name, fontsize=14)
        plt.ylabel('Total Amount', fontsize=14)
        plt.xticks(rotation=45)
    else:
        return None

    file_path = f'static/images/{column_name}_plot.png'
    plt.savefig(file_path, bbox_inches='tight')
    plt.close()
    return file_path

# Home page
@app.route('/')
def index():
    columns = ['Gender', 'Age Group', 'Marital_Status', 'State', 'Occupation', 'Product_Category']
    return render_template('index.html', columns=columns)

# Plot generation route
@app.route('/plot', methods=['POST'])
def plot():
    selected_column = request.form.get('column')
    image_path = generate_plot(selected_column)
    if image_path:
        return render_template('index.html', columns=['Gender', 'Age Group', 'Marital_Status', 'State', 'Occupation',
                                                      'Product_Category'], image_path=image_path, selected_column=selected_column)
    else:
        return "Invalid selection", 400

# Route to add new data
@app.route('/add_data', methods=['POST'])
def add_data():
    try:
        new_data = {
            'Gender': request.form['Gender'],
            'Age Group': request.form['Age_Group'],
            'Marital_Status': request.form['Marital_Status'],
            'State': request.form['State'],
            'Occupation': request.form['Occupation'],
            'Product_Category': request.form['Product_Category'],
            'Amount': int(request.form['Amount'])
        }
        new_df = pd.DataFrame([new_data])
        new_df.to_csv('Diwali Sales Data.csv', mode='a', header=False, index=False)
    except Exception as e:
        return f"Error adding data: {e}", 500

    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
