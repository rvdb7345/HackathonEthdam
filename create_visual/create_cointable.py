import pandas as pd

def create_cointable():

    df = pd.read_csv('data/top10coins_data.csv')

    # Markdown table for the first 3 rows
    markdown_table = "| " + " | ".join(df.columns) + " |\n"
    markdown_table += "| " + " | ".join(['---'] * len(df.columns)) + " |\n"
    for _, row in df.head(3).iterrows():
        markdown_table += "| " + " | ".join(str(cell) for cell in row) + " |\n"

    # Swap columns and rows
    markdown_table_swapped = "|               | "
    markdown_table_swapped += " | ".join(df['Cryptocurrency'].head(3)) + " |\n"
    markdown_table_swapped += "|-------------- |"
    markdown_table_swapped += "-|".join(['-' * len(name) for name in df['Cryptocurrency'].head(3)]) + "--|\n"
    for col_name in df.columns[1:]:
        markdown_table_swapped += "| " + col_name + " | "
        for _, row in df.head(3).iterrows():
            cell = str(row[col_name])
            if col_name == 'Percentage Change':
                cell = "{:.2f}".format(row[col_name])
            markdown_table_swapped += cell + " | "
        markdown_table_swapped += "\n"
    return markdown_table_swapped

if __name__ == "__main__":
    table = create_cointable()
    # Save the Markdown table as a .txt file
    with open('create_visual/table.txt', 'w') as file:
        file.write(table)
    print('Created table')