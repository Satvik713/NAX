import pandas as pd

input_files = [
    '/home/satvik/nax/NAX/ml-1m/ratings.dat',
    '/home/satvik/nax/NAX/ml-1m/movies.dat',
    '/home/satvik/nax/NAX/ml-1m/users.dat'
]

output_files = [
    '/home/satvik/nax/NAX/ml-1m/ratings.csv',
    '/home/satvik/nax/NAX/ml-1m/movies.csv',
    '/home/satvik/nax/NAX/ml-1m/users.csv' 
]


delimiter = '\t' 
def convert_dat_to_csv(input_file, output_file):
    encodings = ['ISO-8859-1', 'latin1', 'utf-8', 'ascii']
    for enc in encodings:
        try:
            df = pd.read_csv(input_file, delimiter=delimiter, encoding=enc)
            df.to_csv(output_file, index=False)
            print(f"File {input_file} converted successfully using {enc} encoding and saved as {output_file}")
            return
        except Exception as e:
            print(f"Failed with encoding {enc}: {e}")
    print(f"All encoding attempts failed for file {input_file}.")

for input_file, output_file in zip(input_files, output_files):
    convert_dat_to_csv(input_file, output_file)
