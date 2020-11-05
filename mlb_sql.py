import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('sqlite://', echo=False)

# convert pandas dataframe into SQL database
df = pd.read_csv('/Users/josephbell/Desktop/sql-practice/mlb.csv')
df = df.rename(columns= {'2B': 'Doubles', '3B': 'Triples'})
df.to_sql('mlb', con=engine)

# convert SQL query into pandas dataframe
df2 = pd.read_sql("SELECT * FROM mlb LIMIT 5;", con=engine)
print(df2)

# equivalent to df.head() in pandas
print(df.head())

# average of stats for all players by season using pandas
print(df.groupby('Season').mean())

# average of stats for all players by season using SQL
df3 = pd.read_sql(
    """SELECT AVG(weight),AVG(height),AVG(G),AVG(AB),AVG(R),AVG(H),AVG(Doubles),AVG(Triples),AVG(HR),AVG(RBI),AVG(SB),AVG(BB),AVG(SO),AVG(salary),AVG(IBB),AVG(HBP),AVG(SH),AVG(SF),AVG(PA)
       FROM mlb
       GROUP BY Season;""", con=engine)
print(df3)

