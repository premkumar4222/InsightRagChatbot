#Ensue pinecone index
import re
from dotenv import load_dotenv
import textwrap
from typing import List,Dict,Any
from openai import OpenAI
load_dotenv()
from pinecone import Pinecone,ServerlessSpec
pc=Pinecone()
def ensure_index(index_name:str,dimension:int =1536, metric:str="cosine"):
    existing={ix['name'] for ix in pc.list_indexes()}
    if index_name not in existing:
        pc.create_index(
        name=index_name,
        dimension=dimension,
        spec=ServerlessSpec(cloud='aws',region='us-east-1'),
        metric=metric
        )
        print("index created")
    return pc.Index(index_name)
index=ensure_index("schemaindex")


#Reading and parsing schema 
with open("docs/schema.txt",'r') as f:
    schema_text=f.read()

schema_rows = [
    # Table: accountWise_Billable
    {"table": "accountWise_Billable", "column": "Date", "type": "Date", "description": "Actual date of billable headcount"},
    {"table": "accountWise_Billable", "column": "Europe", "type": "Integer", "description": "Billable headcount for Europe on that date"},
    {"table": "accountWise_Billable", "column": "America1", "type": "Integer", "description": "Billable headcount for Americas1 on that date"},
    {"table": "accountWise_Billable", "column": "America2", "type": "Integer", "description": "Billable headcount for Americas2 on that date"},
    {"table": "accountWise_Billable", "column": "Apmea", "type": "Integer", "description": "Billable headcount for Apmea on that date"},

    # Table: accountWise_Billable_forecasted
    {"table": "accountWise_Billable_forecasted", "column": "Date", "type": "Date", "description": "Actual date of forecasted billable headcount"},
    {"table": "accountWise_Billable_forecasted", "column": "Europe", "type": "Integer", "description": "Forecasted billable headcount for Europe on that date"},
    {"table": "accountWise_Billable_forecasted", "column": "America1", "type": "Integer", "description": "Forecasted billable headcount for Americas1 on that date"},
    {"table": "accountWise_Billable_forecasted", "column": "America2", "type": "Integer", "description": "Forecasted billable headcount for Americas2 on that date"}]


example_queries=re.split(f"Example Query \d+",schema_text)
example_queries=[q.strip() for q in example_queries if q.strip()]

client=OpenAI()
def embed_text(text:str):
    print("called embed text",text)
    result=client.embeddings.create(
        model='text-embedding-3-small',
        input=text
    ).data[0].embedding
    return result
def col_text_repr(row:Dict[str,Any])->str:
    return textwrap.dedent(f"""\
    Table:{row['table']}
    Column:{row['column']}
    Type:{row.get('type','')}
    Description:{row.get('descriptin','')}""").strip()
def upsert_Schema(schema_rows:List[Dict[str,Any]]):
    vectors=[]
    for r in schema_rows:
        text=col_text_repr(r)
        emb=embed_text(text)
        vectors.append({
            "id":f"schema_{r['table']}.{r['column']}",
            "values":emb,
            "metadata":{"type":"schema","text":text}
        })
    if vectors:
        index.upsert(vectors)
        print("upserted schema rows")
def upsert_examples(example_queries):
    vectors=[]
    for i,q in enumerate(example_queries):
        emb=embed_text(q)
        vectors.append({
            "id":f"example_{i}",
            "values":emb,
            "metadata":{"type":"example","text":q}
        })
    if vectors:
        index.upsert(vectors)
        print("upserted examples")
def retrieve_relevant(state,top_k:int=5):
    print("question",state["question"])
    q_emb=embed_text(state["question"])
    results=index.query(vector=q_emb,top_k=top_k,include_metadata=True)
    state['schema']=results
    return state

#upsert_Schema(schema_rows)
#upsert_examples(example_queries)
#To know inserted or not 
#print(index.describe_index_stats())
# user_question="europe billable headcount prediction next 30 days"
# retrieved=retrieve_relevant(user_question,top_k=6)
#print(retrieved)
