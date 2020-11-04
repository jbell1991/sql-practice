import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite://', echo=False)

# convert pandas dataframe into SQL database
df = pd.read_csv('/Users/josephbell/Desktop/sql-practice/mlb.csv')
df.to_sql('mlb', con=engine)

# convert SQL query into pandas dataframe
df2 = pd.read_sql("SELECT * FROM mlb LIMIT 5", con=engine)
print(df2)