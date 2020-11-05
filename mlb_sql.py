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
average_stats = pd.read_sql("""
    SELECT AVG(weight),AVG(height),AVG(G),AVG(AB),AVG(R),AVG(H),
    AVG(Doubles),AVG(Triples),AVG(HR),AVG(RBI),AVG(SB),AVG(BB),AVG(SO),
    AVG(salary),AVG(IBB),AVG(HBP),AVG(SH),AVG(SF),AVG(PA)
    FROM mlb
    GROUP BY Season;
    """, con=engine)
print(average_stats)

# average of stats for oakland players by season using pandas
oak = df[df['teamID'] == 'OAK']
print(oak.groupby(oak['Season']).mean())

# average of stats for oakland players by season using SQL
oak_stats = pd.read_sql("""
    SELECT AVG(weight),AVG(height),AVG(G),AVG(AB),AVG(R),AVG(H),
    AVG(Doubles),AVG(Triples),AVG(HR),AVG(RBI),AVG(SB),AVG(BB),AVG(SO),
    AVG(salary),AVG(IBB),AVG(HBP),AVG(SH),AVG(SF),AVG(PA)
    FROM mlb
    WHERE teamID = 'OAK'
    GROUP BY Season;
    """, con=engine)
print(oak_stats)

# joining average salary with df on season using pandas
avg_salary = pd.DataFrame(df['salary'].groupby(df['Season']).mean().astype(int))
avg_salary.columns = ['Avg_Salary']
df3 = df.merge(avg_salary, how='inner', on='Season')
print(df3.head())

# joining average salary with df on season using SQL
# create table
avg_salary_sql = pd.read_sql("""
    SELECT Season, AVG(salary)
    FROM mlb
    GROUP BY Season;
    """, con=engine)
avg_salary_sql.to_sql('avg_salary_sql', con=engine)
print(avg_salary_sql)

# join
df_avg_salary = pd.read_sql("""
    SELECT playerID,`Player Name`,weight,height,bats,throws, mlb.Season,
    League,teamID,Team,Franchise,G,AB,R,H,Doubles,Triples,HR,RBI,SB,
    BB,SO,salary,`AVG(Salary)`,IBB,HBP,SH,SF,PA 
    FROM mlb
        JOIN avg_salary_sql ON mlb.Season = avg_salary_sql.Season
    LIMIT 20;
    """, con=engine
)                                                                   
print(df_avg_salary)
