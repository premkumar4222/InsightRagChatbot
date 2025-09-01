from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from pydantic import BaseModel,Field
load_dotenv()

def insightGenerator(state):
    llm=ChatGoogleGenerativeAI(model="gemini-2.0-flash-lite")

    system="""
    You are a data analyst. Given a business question and the result of an SQL query , analyze the data and generate clear, concise, and insightful observations that answer the question.

    Question:
    {question}

    Sql_result:
    {sql_result}

    Your Task:

    Summarize key insights based on the data

    Highlight any trends, outliers, or patterns

    Provide a direct answer to the question if possible

    Keep the response clear, factual, and actionable

    """

    prompt=ChatPromptTemplate.from_messages([
        ('system',system),
        ('human',"question:{question}\nsql_result:{sql_result}")
    ])

    query_writer=prompt | llm

    question=state['question']
    sql_result=state['sql_result']
    res=query_writer.invoke({
        "question":question,
        "sql_result":sql_result
    })
    state['insight']=res
    print(state['insight'])
    return state