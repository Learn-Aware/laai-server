from fastapi import APIRouter, status
from services.health_service import HealthService

router = APIRouter()

@router.get("/database", status_code=status.HTTP_200_OK)
async def check_database_health():
    """
    Check if the MongoDB database connection is healthy.
    Returns 200 OK with different status messages depending on the connection state.
    """
    return await HealthService.check_database_health() 