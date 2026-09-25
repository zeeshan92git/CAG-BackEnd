from pypdf import PdfReader

def extract_text_from_pdf(pdf_path: str):
    """
    Extracts all content from a PDF file using PyPDF
    
    Args: 
        pdf_path (str): Path to the PDF file
        
    Returns: 
        str: The extracted text as a single string, or empty string if extraction fails
    """

    try:
        reader = PdfReader(pdf_path)
        full_text = []

        for page in reader.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)
        return "\n".join(full_text)

    except FileNotFoundError:
        print(f"File not found at {pdf_path}")
        return ""
    except Exception as e:
        print(f"An error occurred while extracting text: {e}")
        return ""
