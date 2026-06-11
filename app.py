from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from agent.agent_workflow import GraphBuilder
from utils.supabase_client import get_supabase
from pydantic import BaseModel
from dotenv import load_dotenv
import datetime
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
async def query_travel_agent(
    query: QueryRequest,
    x_user_id: str = Header(..., description="Device or user ID from Flutter")
):
    try:
        output = react_app.invoke({"messages": [query.question]})
        final_output = (
            output["messages"][-1].content
            if isinstance(output, dict) and "messages" in output
            else str(output)
        )

        # Generate filename
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"AI_Trip_Planner_{timestamp}.md"
        storage_path = f"{x_user_id}/{filename}"

        supabase = get_supabase()

        # Upload .md file to Supabase Storage
        supabase.storage.from_("travel-plans").upload(
            path=storage_path,
            file=final_output.encode("utf-8"),
            file_options={"content-type": "text/markdown"},
        )

        # Save metadata to database
        supabase.table("travel_plans").insert({
            "user_id": x_user_id,
            "question": query.question,
            "answer": final_output,
            "filename": filename,
        }).execute()

        return {
            "answer": final_output,
            "filename": filename,
            "download_url": f"/download/{filename}",
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/history")
async def list_documents(
    x_user_id: str = Header(..., description="Device or user ID from Flutter")
):
    supabase = get_supabase()
    result = (
        supabase.table("travel_plans")
        .select("id, question, filename, created_at")
        .eq("user_id", x_user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return {
        "documents": [
            {
                "filename": row["filename"],
                "question": row["question"],
                "created_at": row["created_at"],
                "download_url": f"/download/{row['filename']}",
            }
            for row in result.data
        ]
    }


@app.get("/download/{filename}")
async def download_document(
    filename: str,
    x_user_id: str = Header(..., description="Device or user ID from Flutter")
):
    supabase = get_supabase()
    storage_path = f"{x_user_id}/{filename}"
    try:
        file_bytes = supabase.storage.from_("travel-plans").download(storage_path)
        return Response(
            content=file_bytes,
            media_type="text/markdown",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )
    except Exception:
        return JSONResponse(status_code=404, content={"error": "File not found"})


@app.get("/health")
async def health():
    return {"status": "ok"}