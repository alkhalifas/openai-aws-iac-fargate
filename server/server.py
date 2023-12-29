from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
import os

# Initialize the FastAPI app
app = FastAPI()


class SummarizeRequest(BaseModel):
    query: str

# Home route
@app.get("/")
async def query_summarize():
    try:
        return {"response": "Welcome to the API!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Route using ChatGPT
@app.get("/api/query/fact")
async def query_summarize(query: str):
    try:
        prompt = ChatPromptTemplate.from_template("Generate a fact about {item}")
        model = ChatOpenAI()
        chain = prompt | model
        response = chain.invoke({"item": query})

        return {"response": response.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
