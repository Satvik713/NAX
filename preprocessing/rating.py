import pandas as pd

input_file = '/home/satvik/nax/NAX/ml-1m/ratings.csv'
data = pd.read_csv(input_file, header=None, names=['combined'])

data[['UserID', 'MovieID', 'Rating', 'Timestamp']] = data['combined'].str.split('::', expand=True)

data.drop('combined', axis=1, inplace=True)
output_file = '/home/satvik/nax/NAX/ml-1m/ratings_1.csv'
data.to_csv(output_file, index=False)
