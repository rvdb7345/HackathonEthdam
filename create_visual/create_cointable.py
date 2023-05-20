import pandas as pd

def create_cointable():

    df = pd.read_csv('data/top10coins_data.csv')

    # Convert the 'Percentage Change' column to string format
    df['Percentage Change'] = df['Percentage Change'].astype(str)

    # Apply formatting to the 'Percentage Change' column based on positive/negative values
    df['Percentage Change'] = df['Percentage Change'].apply(lambda x: f'<span style="color:green">{x}</span>' if float(x) >= 0 else f'<span style="color:red">{x}</span>')

    # Convert the DataFrame to Markdown table format
    markdown_table = df.to_markdown(index=False)

    return markdown_table

if __name__ == "__main__":
    table = create_cointable()
    # Save the Markdown table as a .txt file
    with open('create_visual/table.txt', 'w') as file:
        file.write(table)
