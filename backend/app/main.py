from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, HttpUrl
from app.services.ingestor import RepoIngestor
from app.services.llm_service import AIService
from app.services.rag_service import CodebaseRAGService

app = FastAPI(
    title="DevOps AI Assistant API",
    description="Local AI Engine for Architecture, Security, Q&A, Docs, Cloud & DevOps Automation",
    version="0.5.0"
)

ai_service = AIService(default_coder_model="qwen2.5-coder:7b")
rag_service = CodebaseRAGService(model_name="qwen2.5-coder:7b")

class RepoAnalysisRequest(BaseModel):
    repo_url: HttpUrl

class CodeChatRequest(BaseModel):
    repo_url: HttpUrl
    question: str

@app.get("/")
def root():
    return {"message": "DevOps AI Assistant Backend is live!"}

@app.post("/api/v1/analyze-architecture")
async def analyze_architecture(request: RepoAnalysisRequest):
    repo_url_str = str(request.repo_url)
    ingestor = RepoIngestor(repo_url=repo_url_str)
    
    try:
        ingestor.clone_repository()
        files = ingestor.extract_code_files()
        
        if not files:
            raise HTTPException(status_code=400, detail="No readable code files found in repository.")

        arch_report = ai_service.analyze_architecture(files)
        
        return {
            "status": "success",
            "repo_url": repo_url_str,
            "summary": {
                "parsed_files": len(files),
                "total_lines": sum(f["line_count"] for f in files)
            },
            "architecture_report": arch_report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        ingestor.cleanup()

@app.post("/api/v1/scan-security")
async def scan_security(request: RepoAnalysisRequest):
    repo_url_str = str(request.repo_url)
    ingestor = RepoIngestor(repo_url=repo_url_str)
    
    try:
        ingestor.clone_repository()
        files = ingestor.extract_code_files()
        
        if not files:
            raise HTTPException(status_code=400, detail="No source code files found to scan.")

        security_report = ai_service.scan_repository_security(files)
        
        return {
            "status": "success",
            "repo_url": repo_url_str,
            "summary": {
                "scanned_files": len(files)
            },
            "security_audit_report": security_report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        ingestor.cleanup()

@app.post("/api/v1/chat-codebase")
async def chat_codebase(request: CodeChatRequest):
    repo_url_str = str(request.repo_url)
    ingestor = RepoIngestor(repo_url=repo_url_str)
    
    try:
        ingestor.clone_repository()
        files = ingestor.extract_code_files()
        
        if not files:
            raise HTTPException(status_code=400, detail="No code files available to answer questions.")

        answer = rag_service.answer_question(files=files, question=request.question)
        
        return {
            "status": "success",
            "repo_url": repo_url_str,
            "question": request.question,
            "answer": answer
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        ingestor.cleanup()

@app.post("/api/v1/generate-docs")
async def generate_docs(request: RepoAnalysisRequest):
    repo_url_str = str(request.repo_url)
    ingestor = RepoIngestor(repo_url=repo_url_str)
    
    try:
        ingestor.clone_repository()
        files = ingestor.extract_code_files()
        
        if not files:
            raise HTTPException(status_code=400, detail="No files found to generate documentation.")

        readme_content = ai_service.generate_readme_docs(files)
        
        return {
            "status": "success",
            "repo_url": repo_url_str,
            "readme_md": readme_content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        ingestor.cleanup()

@app.post("/api/v1/cloud-optimizer")
async def cloud_optimizer(request: RepoAnalysisRequest):
    repo_url_str = str(request.repo_url)
    ingestor = RepoIngestor(repo_url=repo_url_str)
    
    try:
        ingestor.clone_repository()
        files = ingestor.extract_code_files()
        
        if not files:
            raise HTTPException(status_code=400, detail="No files found for cloud analysis.")

        cloud_report = ai_service.recommend_cloud_optimization(files)
        
        return {
            "status": "success",
            "repo_url": repo_url_str,
            "cloud_report": cloud_report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        ingestor.cleanup()

@app.post("/api/v1/devops-generator")
async def devops_generator(request: RepoAnalysisRequest):
    repo_url_str = str(request.repo_url)
    ingestor = RepoIngestor(repo_url=repo_url_str)
    
    try:
        ingestor.clone_repository()
        files = ingestor.extract_code_files()
        
        if not files:
            raise HTTPException(status_code=400, detail="No files found for DevOps manifest generation.")

        devops_report = ai_service.generate_devops_manifests(files)
        
        return {
            "status": "success",
            "repo_url": repo_url_str,
            "devops_report": devops_report
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        ingestor.cleanup()