from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from agent.agent_workflow import GraphBuilder
from utils.save_to_document import save_document
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

graph = GraphBuilder()
react_app = graph()

class QueryRequest(BaseModel):
    question: str

@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        messages = {"messages": [query.question]}
        output = react_app.invoke(messages)

        final_output = (
            output["messages"][-1].content
            if isinstance(output, dict) and "messages" in output
            else str(output)
        )

        # Save and include the file path in the response
        saved_path = save_document(final_output)

        return {
            "answer": final_output,
            "document_path": saved_path,
            "download_url": f"/download/{os.path.basename(saved_path)}" if saved_path else None
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/download/{filename}")
async def download_document(filename: str):
    """Endpoint to download a previously generated travel plan"""
    filepath = f"./output/{filename}"
    
    if not os.path.exists(filepath):
        return JSONResponse(status_code=404, content={"error": "File not found"})
    
    return FileResponse(
        path=filepath,
        filename=filename,
        media_type="text/markdown"
    )


@app.get("/history")
async def list_documents():
    """List all previously generated travel plans"""
    output_dir = "./output"
    if not os.path.exists(output_dir):
        return {"documents": []}
    
    files = sorted(os.listdir(output_dir), reverse=True)
    return {
        "documents": [
            {"filename": f, "download_url": f"/download/{f}"}
            for f in files if f.endswith(".md")
        ]
    }