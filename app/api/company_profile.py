from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user_id
from app.core.exceptions import TradeLabException
from app.db.database import get_db
from app.schemas.company_profile import CompanyProfileResponse
from app.services.company_profile_service import CompanyProfileService


router = APIRouter(prefix = "/company_profiles",
					tags = ["Company Profiles"])
service = CompanyProfileService()


@router.get("/{ticker}", response_model = CompanyProfileResponse)
def get_company_profile(ticker: str, db: Session = Depends(get_db),
						user_id: int = Depends(get_current_user_id)):
	return service.get_profile(db, user_id, ticker)


@router.post("/{ticker}/refresh", response_model = CompanyProfileResponse)
def refresh_company_profile(ticker: str, db: Session = Depends(get_db),
							user_id: int = Depends(get_current_user_id)):
	profile = service.sync_profile_from_file(db, ticker)
	if profile is None:
		raise TradeLabException(f"No local company profile available for {ticker}", status_code = 404)
	return profile