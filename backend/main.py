from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Debug print when this module is imported
print(" main.py loaded")

from backend.agent import analyze_code_and_suggest, generate_test_template, update_documentation

# Debug print after successfully importing agent functions
print(" Imported agent functions")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React’s URL
    allow_credentials=True,
    allow_methods=["*"],      # allow all HTTP methods including OPTIONS
    allow_headers=["*"],      # allow all headers
)


class CodeRequest(BaseModel):
    file_path: str

@app.post("/analyze")
async def api_analyze(request: CodeRequest):
    print(" Received /analyze request with:", request.file_path)
    suggestions = analyze_code_and_suggest(request.file_path)
    return {"suggestions": suggestions}

@app.post("/generate-test")
async def api_generate_test(request: CodeRequest):
    print(" Received /generate-test request with:", request.file_path)
    result = generate_test_template(request.file_path)
    return {"result": result}

@app.post("/update-docs")
async def api_update_docs(request: CodeRequest):
    print(" Received /update-docs request with:", request.file_path)
    result = update_documentation(request.file_path)
    return {"result": result}
