from fastapi import APIRouter, HTTPException, Depends, Header, status, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import json

from services.extractor import extract_job_info

extractor_router = APIRouter()

class ExtractRequest(BaseModel):
    """"Schema for the job description extraction request."""
    job_description: str

class ResponseModel(BaseModel):
    """Schema for the response model."""
    position: str
    company: str

@extractor_router.post("/extract-job", response_model=ResponseModel)
async def extract_job(
    request: ExtractRequest, 
    api: str = Header(None),
):
    """Extract job info from job description."""

    # Validate headers and request body
    if not api:
        raise HTTPException(status_code=400, detail="API key header is required")
    
    if not request.job_description:
        raise HTTPException(status_code=400, detail="Job description is required")
    
    # Extract job info using the extractor service
    try:
        extract_info = extract_job_info(request.job_description, api)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting job info: {str(e)}")
    
    # Parse the extracted JSON
    payload = json.loads(extract_info)
    job_title = payload["jobTitle"]
    company = payload["company"]

    print(f"Extracted Job Title: {job_title}, Company: {company}")

    return ResponseModel(position=job_title, company=company)