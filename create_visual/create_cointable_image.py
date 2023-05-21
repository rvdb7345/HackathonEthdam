import pandas as pd
import plotly.figure_factory as ff

def create_cointable_image():
    df = pd.read_csv('data/top10coins_data.csv')
    df_first_5 = df.head(5)
    df_first_5['Cryptocurrency'] = df_first_5['Cryptocurrency'].apply(lambda x: x.capitalize())

    df_transposed = df_first_5.transpose()
    df_transposed.reset_index(inplace=True)
    df_transposed.columns = df_transposed.iloc[0]
    df_transposed = df_transposed.iloc[1:]

    fig = ff.create_table(df_transposed)
    fig.update_layout(
        autosize=False,
        width=800,  # Adjust the width according to your preference
        height=200,
        margin=dict(l=0, r=0, t=0, b=0),
    )

    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 12  # Adjust the font size according to your preference

    fig.write_image("create_visual/table_plotly.png", scale=2)

if __name__ == "__main__":
    table = create_cointable_image()
    print('Finished creating png')

