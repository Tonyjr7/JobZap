from fastapi import APIRouter, HTTPException, Depends, Header, status, Query
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
    company: str
    position: str
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
    if not request.position or not request.company:
        raise HTTPException(status_code=400, detail="Job description is required")

    # Check if the company already exists in the database 10 days ago
    fifteen_days_ago = datetime.utcnow() - timedelta(days=15)

    existing_job = db.query(Job).filter(
        Job.company == request.company,
        Job.date_added >= fifteen_days_ago
    ).first()
    if existing_job and not request.force_save:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=ResponseModel(
                message=f"{request.company} company already exists in the database within the last 15 days",
                company=request.company
            ).dict()
        )

    # Save the new job to the database
    try:
        new_job = Job(
            job_title=request.position, 
            company=request.company, 
            job_url=request.job_url
        )

        db.add(new_job)

        send_discord_notification(request.position, request.company, request.job_url, request.webhooks, request.user, request.force_save)

        db.commit()
        db.refresh(new_job)

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error saving to database: {str(e)}")

    return {"message": f"{request.company} added successfully", "company": request.company}

@router.get("/forward-job")
async def forward_job(
    db: Session = Depends(get_db),
    after_id: int = Query(0, description="Fetch jobs with ID greater than this"),
    limit: int = Query(50, description="Maximum number of jobs to fetch")
):
    try:
        jobs_query = db.query(Job).filter(Job.id > after_id).order_by(Job.id.asc()).limit(limit)
        jobs = jobs_query.all()

        job_list = []
        for job in jobs:
            job_list.append({
                "id": job.id,
                "position": getattr(job, "position", getattr(job, "job_title", None)),
                "company": getattr(job, "company", None),
                "job_url": getattr(job, "job_url", None),
                "date_added": job.date_added.isoformat() if getattr(job, "date_added", None) else None
            })

        return {"jobs": job_list}

    except Exception as e:
        # Log the error for debugging
        import traceback
        print("Error in forward_job:", traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Error fetching jobs: {str(e)}")