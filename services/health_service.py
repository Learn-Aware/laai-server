from typing import Dict, Any
from dal import health_dal

class HealthService:
    """Service for health check operations"""
    
    @staticmethod
    async def check_database_health() -> Dict[str, Any]:
        """Check the health of the database connection"""
        return await health_dal.check_database_health() 