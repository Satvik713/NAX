import pandas as pd

input_file = '/home/satvik/nax/NAX/ml-1m/movies.csv'
data = pd.read_csv(input_file, header=None, names=['combined'])
data[['MovieID', 'Title', 'Genres']] = data['combined'].str.split('::', expand=True)
data.drop('combined', axis=1, inplace=True)

output_file = '/home/satvik/nax/NAX/ml-1m/movies_1.csv'
data.to_csv(output_file, index=False)
