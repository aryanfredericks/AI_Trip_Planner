from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, Response
from agent.agent_workflow import GraphBuilder
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

OUTPUT_DIR = "output"
os.makedirs(OUTPUT_DIR, exist_ok=True)


class QueryRequest(BaseModel):
    question: str


# ── Endpoints ──────────────────────────────────────────────────────────────
@app.post("/query")
async def query_travel_agent(query: QueryRequest):
    try:
        output = react_app.invoke({"messages": [query.question]})
        final_output = (
            output["messages"][-1].content
            if isinstance(output, dict) and "messages" in output
            else str(output)
        )

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"AI_Trip_Planner_{timestamp}.md"
        file_path = os.path.join(OUTPUT_DIR, filename)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(final_output)

        return {
            "answer": final_output,
            "filename": filename,
            "download_url": f"/download/{filename}",
        }

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/history")
async def list_documents():
    files = []
    for filename in sorted(os.listdir(OUTPUT_DIR), reverse=True):
        if filename.endswith(".md"):
            file_path = os.path.join(OUTPUT_DIR, filename)
            created_at = datetime.datetime.fromtimestamp(
                os.path.getctime(file_path)
            ).isoformat()
            files.append({
                "filename": filename,
                "created_at": created_at,
                "download_url": f"/download/{filename}",
            })
    return {"documents": files}


@app.get("/download/{filename}")
async def download_document(filename: str):
    # Sanitise to prevent path traversal
    filename = os.path.basename(filename)
    file_path = os.path.join(OUTPUT_DIR, filename)

    if not os.path.exists(file_path):
        return JSONResponse(status_code=404, content={"error": "File not found"})

    with open(file_path, "rb") as f:
        content = f.read()

    return Response(
        content=content,
        media_type="text/markdown",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )


@app.get("/health")
async def health():
    return {"status": "ok"}