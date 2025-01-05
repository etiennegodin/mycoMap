import pandas as pd


excel_file = './data/testExport.xlsx'
# Read the Excel file into a pandas DataFrame
df = pd.read_excel(excel_file)

# Replace 'output_file.csv' with the desired name for your CSV file
csv_file = 'testOuput.csv'


# Write the DataFrame to a CSV file
df.to_csv(csv_file, index=False, encoding='utf-8')