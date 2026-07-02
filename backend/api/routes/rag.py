import os
import shutil
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from auth.jwt.auth_dependency import get_current_user
from rag.ingestion.document_ingestion import DocumentIngestion

from rag.loaders.loader_factory import LoaderFactory

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    project: str = None,
    current_user = Depends(get_current_user)
):
    print(f"\n[RAG Route] Received upload request for file: {file.filename}")
    # Verify file extension dynamically from LoaderFactory registry
    supported = LoaderFactory.supported_extensions()
    _, ext = os.path.splitext(file.filename.lower())
    if ext not in supported:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format '{ext}'. Supported formats: {', '.join(supported)}"
        )
        
    # Save file to a temporary directory
    upload_dir = "uploads/documents"
    os.makedirs(upload_dir, exist_ok=True)
    temp_path = os.path.join(upload_dir, file.filename)
    
    try:
        print(f"[RAG Route] Saving file locally to: {temp_path}")
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Ingest the document
        print("[RAG Route] File saved. Instantiating DocumentIngestion...")
        ingestor = DocumentIngestion()
        print("[RAG Route] Starting document ingestion...")
        chunks_inserted = ingestor.ingest(
            file_path=temp_path,
            project=project,
            user_id=current_user.id
        )
        print(f"[RAG Route] Ingestion completed. Chunks inserted: {chunks_inserted}")
        
        return {
            "status": "success",
            "message": f"Successfully ingested {file.filename}",
            "chunks_inserted": chunks_inserted
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.remove(temp_path)
