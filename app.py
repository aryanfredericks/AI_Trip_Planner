from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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

bearer = HTTPBearer()


# ── Auth dependency ────────────────────────────────────────────────────────
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer)
):
    """Validates the Supabase JWT sent from Flutter and returns the user ID."""
    token = credentials.credentials
    supabase = get_supabase()
    try:
        response = supabase.auth.get_user(token)
        if not response or not response.user:
            raise HTTPException(status_code=401, detail="Invalid token")
        return response.user.id   # returns the Supabase user UUID
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


class QueryRequest(BaseModel):
    question: str


# ── Endpoints ──────────────────────────────────────────────────────────────
@app.post("/query")
async def query_travel_agent(
    query: QueryRequest,
    user_id: str = Depends(get_current_user)   # ✅ replaces x_user_id header
):
    try:
        output = react_app.invoke({"messages": [query.question]})
        final_output = (
            output["messages"][-1].content
            if isinstance(output, dict) and "messages" in output
            else str(output)
        )

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"AI_Trip_Planner_{timestamp}.md"
        storage_path = f"{user_id}/{filename}"

        supabase = get_supabase()

        supabase.storage.from_("travel-plans").upload(
            path=storage_path,
            file=final_output.encode("utf-8"),
            file_options={"content-type": "text/markdown"},
        )

        supabase.table("travel_plans").insert({
            "user_id": user_id,
            "question": query.question,
            "answer": final_output,
            "filename": filename,
            "storage_path": storage_path,
        }).execute()

        return {
            "answer": final_output,
            "filename": filename,
            "download_url": f"/download/{filename}",
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/history")
async def list_documents(user_id: str = Depends(get_current_user)):
    supabase = get_supabase()
    result = (
        supabase.table("travel_plans")
        .select("id, question, filename, created_at")
        .eq("user_id", user_id)
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
    user_id: str = Depends(get_current_user)
):
    supabase = get_supabase()
    storage_path = f"{user_id}/{filename}"
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