from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException,
    Query,
)

import uuid as uuid_pkg
import os


from src.data_store import data_store
from src.utils.pdf_processor import extract_text_from_pdf
from src.utils.llm_client import get_llm_response


router = APIRouter()


UPLOAD_DIR = "/tmp/cag_uploads"

os.makedirs(
    UPLOAD_DIR,
    exist_ok=True,
)


# ─────────────────────────────────────────────────────────────
# PDF VALIDATION
# ─────────────────────────────────────────────────────────────

def read_and_validate_pdf(
    file: UploadFile
) -> tuple[str, bytes]:
    """
    Validate that uploaded content is actually a PDF.

    Returns:
        safe filename
        file bytes
    """

    filename = os.path.basename(
        file.filename or ""
    )


    # Extension validation
    if not filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only .pdf files are allowed."
        )


    file_bytes = file.file.read()


    if not file_bytes:

        raise HTTPException(
            status_code=400,
            detail="Uploaded PDF is empty."
        )


    # Actual PDF file signature validation
    if b"%PDF-" not in file_bytes[:1024]:

        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid PDF file. "
                "The uploaded file does not contain "
                "a valid PDF signature."
            )
        )


    return filename, file_bytes


# ─────────────────────────────────────────────────────────────
# CREATE FIRST DOCUMENT
# ─────────────────────────────────────────────────────────────

@router.post(
    "/upload/{uuid}",
    status_code=201
)
def create_pdf_entry(
    uuid: uuid_pkg.UUID,
    file: UploadFile = File(...)
):
    """
    Create new hidden document context.
    """

    uuid_str = str(uuid)


    if uuid_str in data_store:

        raise HTTPException(
            status_code=400,
            detail=(
                f"UUID {uuid_str} already exists."
            )
        )


    filename, file_bytes = read_and_validate_pdf(
        file
    )


    file_path = os.path.join(
        UPLOAD_DIR,
        f"{uuid_str}_{filename}"
    )


    try:

        # Save temporarily
        with open(file_path, "wb") as buffer:
            buffer.write(file_bytes)


        extracted_text = extract_text_from_pdf(
            file_path
        )


        if not extracted_text:

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text could be extracted "
                    "from this PDF."
                )
            )


        # Store only extracted text.
        data_store[uuid_str] = extracted_text


        return {
            "message": (
                "File uploaded and text extracted successfully."
            ),
            "uuid": uuid_str,
        }


    except HTTPException:
        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "An error occurred during PDF processing: "
                f"{str(e)}"
            )
        )


    finally:

        if os.path.exists(file_path):
            os.remove(file_path)


# ─────────────────────────────────────────────────────────────
# APPEND ANOTHER DOCUMENT
# ─────────────────────────────────────────────────────────────

@router.put("/upload/{uuid}")
def append_pdf_data(
    uuid: uuid_pkg.UUID,
    file: UploadFile = File(...)
):
    """
    Append another PDF's text to existing context.
    """

    uuid_str = str(uuid)


    if uuid_str not in data_store:

        raise HTTPException(
            status_code=400,
            detail="Current document context no longer exists."
        )


    filename, file_bytes = read_and_validate_pdf(
        file
    )


    file_path = os.path.join(
        UPLOAD_DIR,
        f"{uuid_str}_{filename}"
    )


    try:

        with open(file_path, "wb") as buffer:
            buffer.write(file_bytes)


        new_text = extract_text_from_pdf(
            file_path
        )


        if not new_text:

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text could be extracted "
                    "from this PDF."
                )
            )


        # This is your existing CAG append behaviour:
        #
        # doc1 text
        # +
        # doc2 text

        data_store[uuid_str] += (
            "\n\n" + new_text
        )


        return {
            "message": "PDF added successfully.",
            "uuid": uuid_str,
        }


    except HTTPException:
        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=(
                "An error occurred during PDF processing: "
                f"{str(e)}"
            )
        )


    finally:

        if os.path.exists(file_path):
            os.remove(file_path)


# ─────────────────────────────────────────────────────────────
# QUERY CURRENT DOCUMENT CONTEXT
# ─────────────────────────────────────────────────────────────

@router.post("/query/{uuid}")
def query_pdf_content(
    uuid: uuid_pkg.UUID,
    query: str = Query(
        ...,
        min_length=1
    )
):
    """
    Query the current hidden document context.
    """

    uuid_str = str(uuid)


    if uuid_str not in data_store:

        raise HTTPException(
            status_code=400,
            detail=(
                "Document context no longer exists. "
                "Please upload the PDF again."
            )
        )


    stored_text = data_store[uuid_str]


    try:

        llm_response = get_llm_response(
            context=stored_text,
            query=query,
        )


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=f"LLM request failed: {str(e)}"
        )


    return {
        "uuid": uuid_str,
        "query": query,
        "llm_response": llm_response,
    }


# ─────────────────────────────────────────────────────────────
# DELETE CURRENT DOCUMENT CONTEXT
# ─────────────────────────────────────────────────────────────

@router.delete(
    "/data/{uuid}",
    status_code=200
)
def delete_pdf_data(
    uuid: uuid_pkg.UUID
):
    """
    Delete current hidden document context.
    """

    uuid_str = str(uuid)


    if uuid_str not in data_store:

        raise HTTPException(
            status_code=400,
            detail="Document context does not exist."
        )


    del data_store[uuid_str]


    return {
        "message": "Document context cleared successfully."
    }