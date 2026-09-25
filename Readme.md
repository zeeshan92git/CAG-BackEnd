# CAG Project - Chat with PDF API

A FastAPI-based REST API that allows users to upload PDF files, extract text content, and query that content using an LLM (Large Language Model).

## Features

- **PDF Upload**: Upload PDF files with unique UUID identifiers
- **Text Extraction**: Automatically extract text from uploaded PDFs
- **Multi-file Support**: Append multiple PDFs to the same UUID
- **LLM Integration**: Query PDF content using natural language
- **Data Management**: Delete stored data when no longer needed
- **UUID Listing**: View all stored UUIDs

## Project Structure

```
.
├── main.py                 # FastAPI application entry point
├── datahandler.py          # API endpoints/routes
├── data_store.py           # In-memory data storage (dict)
├── pdf_processor.py        # PDF text extraction utility
├── llm_client.py           # LLM integration (placeholder)
├── requirements.txt        # Python dependencies
└── Readme.md              # This file
```

## Setup & Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation Steps

1. **Clone/Download the project** and navigate to the project directory:
   ```bash
   cd cag_project
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the FastAPI server:

```bash
python main.py
```

The server will run on `http://127.0.0.1:8001`

### Access the API

- **Interactive Swagger UI**: http://127.0.0.1:8001/docs
- **ReDoc Documentation**: http://127.0.0.1:8001/redoc
- **Root Endpoint**: http://127.0.0.1:8001/

```

---


## Important Notes

⚠️ **Current Limitations:**

1. **In-Memory Storage**: Data is stored in a Python dictionary and will be lost when the server restarts. For production, use a database (PostgreSQL, MongoDB, etc.).

2. **Temporary Files**: Uploaded PDFs are stored temporarily in `/tmp/cag_uploads` and deleted after processing.

3. **No Authentication**: The API has no authentication. Add JWT or API key validation for production use.

4. **LLM Placeholder**: The `llm_client.py` needs to be configured with a real LLM API.

---

## Error Handling

The API returns appropriate HTTP status codes:

- `200`: Success
- `201`: Created (file uploaded successfully)
- `400`: Bad Request (invalid file type, UUID doesn't exist, etc.)
- `500`: Internal Server Error (PDF extraction failed, etc.)

---

## Development & Testing

### Test with Swagger UI
1. Open http://127.0.0.1:8001/docs
2. Expand each endpoint
3. Click "Try it out"
4. Fill in parameters and upload files

### Generate Test UUID

```python
import uuid
print(uuid.uuid4())
```

---

## Next Steps

1. Configure the LLM integration in `llm_client.py`
2. Add database support instead of in-memory storage
3. Add authentication (JWT tokens)
4. Add request logging and monitoring
5. Deploy to production (AWS, GCP, Azure, etc.)

---

## Dependencies

See `requirements.txt` for full list. Key packages:

- **fastapi**: Web framework
- **uvicorn**: ASGI server
- **pypdf**: PDF text extraction
- **pydantic**: Data validation

---

## License

This project is part of the CAG initiative.

---

## Support

For issues or questions, refer to:
- FastAPI Docs: https://fastapi.tiangolo.com/
- PyPDF Docs: https://pypdf.readthedocs.io/
