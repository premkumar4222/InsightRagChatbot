import pandas as pd
from sqlalchemy import create_engine
data=pd.read_excel("data/accountWise_Billable.xlsx")

print(data.columns)

engine = create_engine("sqlite:///my_database.db")

data.to_sql("accountWise_Billable",con=engine,if_exists="replace",index=False)

query = "SELECT Date, Europe FROM accountWise_Billable WHERE Date >= CURRENT_DATE AND Date <= CURRENT_DATE + INTERVAL('30 days') ORDER BY Date;"

result = pd.read_sql_query(query, con=engine)
print(result)
























