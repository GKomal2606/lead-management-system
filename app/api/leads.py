from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models import Lead, User
from app.schemas import LeadCreate, LeadUpdate, LeadResponse
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/leads", tags=["Lead Management"])

@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
def create_lead(
    lead_data: LeadCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new lead
    
    The lead will be owned by the current logged-in user
    """
    new_lead = Lead(
        full_name=lead_data.full_name,
        email=lead_data.email,
        phone=lead_data.phone,
        company=lead_data.company,
        position=lead_data.position,
        status=lead_data.status,
        notes=lead_data.notes,
        owner_id=current_user.id  # Automatically assign to current user
    )
    
    db.add(new_lead)
    db.commit()
    db.refresh(new_lead)
    
    return new_lead

@router.get("/", response_model=List[LeadResponse])
def list_leads(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    status: str = None
):
    """
    List leads owned by current user
    
    Query parameters:
    - skip: Pagination offset
    - limit: Max records to return
    - status: Filter by lead status (optional)
    
    Regular users see only their leads
    Admins see all leads
    """
    query = db.query(Lead)
    
    # Regular users only see their own leads
    if not current_user.is_admin:
        query = query.filter(Lead.owner_id == current_user.id)
    
    # Filter by status if provided
    if status:
        query = query.filter(Lead.status == status)
    
    leads = query.offset(skip).limit(limit).all()
    return leads

@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get specific lead by ID
    
    Users can only access their own leads
    Admins can access any lead
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    # Check ownership (unless admin)
    if not current_user.is_admin and lead.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this lead"
        )
    
    return lead

@router.patch("/{lead_id}", response_model=LeadResponse)
def update_lead(
    lead_id: int,
    lead_data: LeadUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update a lead
    
    Users can only update their own leads
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    # Check ownership (unless admin)
    if not current_user.is_admin and lead.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this lead"
        )
    
    # Update fields if provided
    update_data = lead_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lead, field, value)
    
    db.commit()
    db.refresh(lead)
    
    return lead

@router.delete("/{lead_id}")
def delete_lead(
    lead_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a lead
    
    Users can only delete their own leads
    """
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found"
        )
    
    # Check ownership (unless admin)
    if not current_user.is_admin and lead.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this lead"
        )
    
    db.delete(lead)
    db.commit()
    
    return {"message": f"Lead {lead.full_name} deleted successfully"}