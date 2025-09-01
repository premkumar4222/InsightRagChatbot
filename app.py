from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from main import revoke_graph
# For async LangGraph call — insert your logic here
# from your_langgraph_module import run_langgraph_app

app = FastAPI()

# CORS setup to allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

@app.post("/chatbot")
async def chatbot(request: ChatRequest):
    user_message = request.message

    # TODO: Replace this with your actual LangGraph call
    # response = await run_langgraph_app(user_message)
    response=revoke_graph(user_message)
    # TEMP RESPONSE (fake)
    #response = f"You said: {user_message}. (This would be from LangGraph)"

    return {"response": response}
