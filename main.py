from fastapi import FastAPI
from src.routers import data_handler
from fastapi.responses import HTMLResponse

app = FastAPI(
    title="CAG Project API Chat with your PDF",
    description="API for uploading PDFs, querying content via LLM, and managing data.",
    version="0.1.0"
)

app.include_router(
    data_handler.router,
    prefix="/api/v1",
    tags=["Data Handling and Chat with PDF"]
)

@app.get("/", response_class=HTMLResponse, tags=["Root"])
def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>CAG Project - Chat with PDF API</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f5f5f5; }
            .container { max-width: 800px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
            h1 { color: #333; }
            p { color: #666; line-height: 1.6; }
            .endpoint { background-color: #f0f0f0; padding: 10px; margin: 10px 0; border-left: 4px solid #007bff; }
            a { color: #007bff; text-decoration: none; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>CAG Project - Chat with Your PDF</h1>
            <p>Welcome to the CAG Project API! This API allows you to upload PDF files, extract text, and query the content using an LLM.</p>
            
            <h2>Available Endpoints:</h2>
            <div class="endpoint">
                <strong>POST /api/v1/upload/{uuid}</strong><br>
                Upload a PDF file for a specific UUID. (Creates new entry)
            </div>
            <div class="endpoint">
                <strong>PUT /api/v1/upload/{uuid}</strong><br>
                Append PDF content to an existing UUID.
            </div>
            <div class="endpoint">
                <strong>POST /api/v1/query/{uuid}</strong><br>
                Query the PDF content using natural language.
            </div>
            <div class="endpoint">
                <strong>DELETE /api/v1/data/{uuid}</strong><br>
                Delete stored data for a specific UUID.
            </div>
            <h2>Getting Started:</h2>
            <p>Visit <a href="/docs">/docs</a> for interactive API documentation (Swagger UI).</p>
            <p>Or visit <a href="/redoc">/redoc</a> for ReDoc documentation.</p>
        </div>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)

# This block runs the server
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app, host="127.0.0.1", port=8001
    )
