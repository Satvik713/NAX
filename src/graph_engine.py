import pandas as pd
import torch
from torch_geometric.data import HeteroData
from sklearn.preprocessing import LabelEncoder, StandardScaler

def _series_to_tensor(series):
    if is_categorical(series): return torch.LongTensor(series.cat.codes.values.astype("int64"))
    else:  return torch.FloatTensor(series.values)

user_df = pd.read_csv('/home/satvik/nax/NAX/ml-1m/users_1.csv')
item_df = pd.read_csv('/home/satvik/nax/NAX/ml-1m/movies_1.csv')
user_item_df = pd.read_csv('/home/satvik/nax/NAX/ml-1m/ratings_1.csv')

user_df.columns = user_df.columns.str.strip()
item_df.columns = item_df.columns.str.strip()
user_item_df.columns = user_item_df.columns.str.strip()

user_mapping = {id: idx for idx, id in enumerate(user_df['UserID'].unique())}
movie_mapping = {id: idx for idx, id in enumerate(item_df['MovieID'].unique())}

user_item_df['UserIndex'] = user_item_df['UserID'].map(user_mapping)
user_item_df['MovieIndex'] = user_item_df['MovieID'].map(movie_mapping)

data = HeteroData()

user_features = user_df.copy()
user_features['Gender'] = LabelEncoder().fit_transform(user_features['Gender'])
user_features = user_features[['Gender', 'Age', 'Occupation']].values
user_features = StandardScaler().fit_transform(user_features)

data['user'].x = torch.tensor(user_features, dtype=torch.float)

item_features = item_df.copy()
genres = item_features['Genres'].str.get_dummies('|')
item_features = pd.concat([item_features, genres], axis=1)
item_features = item_features.drop(columns=['Title', 'Genres'])
item_features = item_features.values
item_features = StandardScaler().fit_transform(item_features)

data['movie'].x = torch.tensor(item_features, dtype=torch.float)
edge_index = torch.tensor([user_item_df['UserIndex'].values, user_item_df['MovieIndex'].values], dtype=torch.long)
data['user', 'rates', 'movie'].edge_index = edge_index

torch.save(data, '/home/satvik/nax/NAX/graphs/movie_lens_1m.pt')

