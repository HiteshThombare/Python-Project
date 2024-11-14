import pandas as pd
import matplotlib.pyplot as plt

# Load and preprocess dataset
df = pd.read_csv('Diwali Sales Data.csv', encoding='unicode_escape')
df.drop(['Status', 'unnamed1'], axis=1, inplace=True)
df.dropna(inplace=True)
df['Amount'] = df['Amount'].astype(int)

# Function to generate a plot based on the selected column
def generate_plot(column_name):
    plt.figure(figsize=(10, 6))
    plt.style.use('seaborn-v0_8-whitegrid')

    # Check if the column is valid for plotting
    if column_name in ['Gender', 'Age Group', 'Marital_Status', 'State', 'Occupation', 'Product_Category']:
        df.groupby(column_name)['Amount'].sum().plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title(f'Total Amount by {column_name}', fontsize=16)
        plt.xlabel(column_name, fontsize=14)
        plt.ylabel('Total Amount', fontsize=14)
        plt.xticks(rotation=45)
    else:
        return None

    # Save the plot to a file
    file_path = f'static/images/{column_name}_plot.png'
    plt.savefig(file_path, bbox_inches='tight')
    plt.close()
    return file_path

# Function to get the available matplotlib styles
def get_styles():
    return plt.style.available
