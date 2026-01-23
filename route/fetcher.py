from fastapi import APIRouter, HTTPException, Depends, Header, status, Response
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.database import get_db
from pydantic import BaseModel
import json
from datetime import datetime, timedelta

from database.models.job import Job
from services.extractor import extract_job_info
from services.discord import send_discord_notification

router = APIRouter()

class AddRequest(BaseModel):
    """"Schema for the job addition request."""
    job_description: str
    job_url: str
    user: str
    webhooks: list[str]
    force_save: bool = False

class ResponseModel(BaseModel):
    """Schema for the response model."""
    message: str
    company: str

@router.post("/post-job")
async def fetch_company(
    request: AddRequest, 
    db: Session = Depends(get_db),
    api: str = Header(None),
):
    """Fetch company info from job description and store it in the database."""

    # Validate headers and request body
    if not api or not request.webhooks:
        raise HTTPException(status_code=400, detail="API key and Webhook URL headers are required")
    
    # Validate job description
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

    # Check if the company already exists in the database 10 days ago
    fifteen_days_ago = datetime.utcnow() - timedelta(days=15)

    existing_job = db.query(Job).filter(
        Job.company == company,
        Job.date_added >= fifteen_days_ago
    ).first()
    if existing_job and not request.force_save:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ResponseModel(
                message=f"{company} company already exists in the database within the last 15 days",
                company=company
            ).dict()
        )

    # Save the new job to the database
    try:
        new_job = Job(
            job_title=job_title, 
            company=company, 
            job_url=request.job_url
        )

        db.add(new_job)

        send_discord_notification(job_title, company, request.job_url, request.webhooks, request.user, request.force_save)

        db.commit()
        db.refresh(new_job)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving to database: {str(e)}")

    return {"message": f"{company} added successfully", "company": company}
