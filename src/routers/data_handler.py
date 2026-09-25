from fastapi import APIRouter, UploadFile, File, HTTPException, Query
import uuid as uuid_pkg
import os

# Import the shared data store
from src.data_store import data_store

# PDF processing utility
from src.utils.pdf_processor import extract_text_from_pdf

# LLM Client utility
from src.utils.llm_client import get_llm_response

router = APIRouter()

# Define temp directory for uploads
UPLOAD_DIR = "/tmp/cag_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/upload/{uuid}", status_code=201)
def create_pdf_entry(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):
    """
    Uploads PDF file with a specific UUID.
    Extracts data and stores in data store.
    If UUID already exists, raises an error.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only PDF files allowed."
        )

    uuid_str = str(uuid)
    if uuid_str in data_store:
        raise HTTPException(
            status_code=400,
            detail=f"UUID {uuid_str} already exists. Use PUT /api/v1/upload/{uuid_str} to append data."
        )
    
    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str}_{file.filename}")
    try:
        # Save the uploaded file temporarily
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        extracted_text = extract_text_from_pdf(file_path)

        if extracted_text is None:
            raise HTTPException(
                status_code=500, 
                detail="Failed to extract text from PDF"
            )

        data_store[uuid_str] = extracted_text
        return {
            "message": "File uploaded and text extracted successfully.",
            "uuid": uuid_str
        }
    except Exception as e:
        # Log the exception
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during file processing: {str(e)}"
        )
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
        

@router.put("/upload/{uuid}")
def append_pdf_data(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):
    """
    Appends new PDF content to an existing UUID.
    If UUID doesn't exist, raises an error.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, 
            detail="Invalid file type. Only PDF files allowed."
        )
    
    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=400,
            detail=f"UUID {uuid_str} doesn't exist. Use POST /api/v1/upload/{uuid_str} to create it first."
        )
    
    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str}_{file.filename}")
    try:
        # Save the uploaded file temporarily
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        new_text = extract_text_from_pdf(file_path)

        if new_text is None:
            raise HTTPException(
                status_code=500, 
                detail="Failed to extract text from PDF"
            )
        
        # Append new text with proper separator
        data_store[uuid_str] += "\n\n" + new_text
        return {
            "message": "Data appended successfully.",
            "uuid": uuid_str
        }
    except Exception as e:
        # Log the exception
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during file processing: {str(e)}"
        )
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            os.remove(file_path)


@router.post("/query/{uuid}")
def query_pdf_content(uuid: uuid_pkg.UUID, query: str = Query(..., min_length=1)):
    """
    Retrieves stored text for a specific UUID and sends it along with the query
    to the LLM, returning the LLM's response.
    """

    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=400,
            detail=f"UUID {uuid_str} doesn't exist."
        )
    
    stored_text = data_store[uuid_str]

    llm_response = get_llm_response(context=stored_text, query=query)

    return {
        "uuid": uuid_str, 
        "query": query, 
        "llm_response": llm_response
    }


@router.delete("/data/{uuid}", status_code=200)
def delete_pdf_data(uuid: uuid_pkg.UUID):
    """
    Delete data associated with a specific UUID from data_store.
    """

    uuid_str = str(uuid)
    if uuid_str not in data_store:
        raise HTTPException(
            status_code=400,
            detail=f"UUID {uuid_str} doesn't exist."
        )
    
    del data_store[uuid_str]
    return {"message": f"Data for UUID {uuid_str} deleted successfully"}


@router.get("/list/uuids")
def list_all_uuids():
    """
    Returns a list of all UUIDs currently stored.
    """
    return {"uuids": list(data_store.keys())}
