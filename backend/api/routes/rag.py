import os
import shutil
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from auth.jwt.auth_dependency import get_current_user
from rag.ingestion.document_ingestion import DocumentIngestion

from rag.loaders.loader_factory import LoaderFactory
from services.data_science_service import DataScienceService

router = APIRouter()


@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    
    project: str = None,
    current_user = Depends(get_current_user)
):
    print(f"\n[RAG Route] Received upload request for file: {file.filename}", flush=True)
    
    _, ext = os.path.splitext(file.filename.lower())
    
    # Smart Dataset Router for Tabular files
    DS_EXTENSIONS = {".csv", ".xlsx", ".xls", ".parquet", ".feather", ".tsv"}
    is_tabular = ext in DS_EXTENSIONS or (file.content_type and "csv" in file.content_type) or (file.content_type and "spreadsheet" in file.content_type)
    
    if is_tabular:
        print(f"[RAG Route] Tabular dataset detected: {file.filename}. Routing to Data Science Service.", flush=True)
        upload_dir = "uploads/datasets"
        os.makedirs(upload_dir, exist_ok=True)
        ds_file_path = os.path.join(upload_dir, file.filename)
        
        try:
            print(f"[RAG Route] Saving dataset to: {ds_file_path}", flush=True)
            with open(ds_file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Execute AutoML pipeline directly via local Python service
            print("[RAG Route] Triggering Data Science Service analyze_dataset...", flush=True)
            service = DataScienceService()
            report = service.analyze_dataset(ds_file_path)
            print("[RAG Route] AutoML pipeline finished successfully.", flush=True)
            
            return {
                "status": "success",
                "route": "data_science",
                "message": f"Successfully processed tabular dataset {file.filename} through AutoML.",
                "data": report
            }
        except Exception as e:
            print(f"[RAG Route Error] Data Science pipeline failed: {str(e)}", flush=True)
            raise HTTPException(status_code=500, detail=f"Data Science pipeline execution failed: {str(e)}")

    # Verify file extension dynamically from LoaderFactory registry
    supported = LoaderFactory.supported_extensions()
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
        print(f"[RAG Route] Saving file locally to: {temp_path}", flush=True)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Ingest the document
        print("[RAG Route] File saved. Instantiating DocumentIngestion...", flush=True)
        ingestor = DocumentIngestion()
        print("[RAG Route] Starting document ingestion...", flush=True)
        chunks_inserted = ingestor.ingest(
            file_path=temp_path,
            project=project,
            user_id=current_user.id
        )
        print(f"[RAG Route] Ingestion completed. Chunks inserted: {chunks_inserted}", flush=True)
        
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
