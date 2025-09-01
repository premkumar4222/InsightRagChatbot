from schemaVectorStore import retrieve_relevant
from sqlQueryGenerator import natural_to_sql
from insightGenerator import insightGenerator
from load_excel_to_sql import quering_sql
from typing import  TypedDict,List
from langgraph.graph import StateGraph , START,END,add_messages


class GraphState(TypedDict):
    question:str
    sql_query:str
    schema:List[str]
    sql_result:str
    insight:str

graph=StateGraph(GraphState)

graph.add_node("retrieve",retrieve_relevant)
graph.add_node("natural_to_sql",natural_to_sql)
graph.add_node("query",quering_sql)
graph.add_node("generatingInsight",insightGenerator)

graph.add_edge("retrieve","natural_to_sql")

graph.add_edge("natural_to_sql","query")

graph.add_edge("query","generatingInsight")

graph.set_entry_point("retrieve")

graph.set_finish_point("generatingInsight")

app=graph.compile()

def revoke_graph(question):
    result=app.invoke({"question":question})
    return result["insight"]
revoke_graph("billable headcount of europe june month")