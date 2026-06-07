import sys, os

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

from Backend.app.Gen_AI.generate_post import generate_json_response

from fastapi import FastAPI, HTTPException # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore

from pydantic import BaseModel, Field

class Generate_Posts_Input(BaseModel):
    platform: str=Field(description="name of the platform")
    post_title: str=Field(description="title of the post")
    tone: str=Field(description="tone of the post")

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # your React app URL
    allow_methods=["*"],      # allow all methods (GET, POST, PUT, DELETE)
    allow_headers=["*"],      # allow all headers
)

@app.post('/generate-post')
def gen_post(data:Generate_Posts_Input):
    if not all([data.platform.strip(), data.post_title.strip(), data.tone.strip()]):
        raise HTTPException(status_code=400, detail="Missing required fields")
    response=generate_json_response(data)
    return response