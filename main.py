import uvicorn
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from controllers.socratic_tutor_controller import router as socratic_tutor_router
from controllers.cached_augmented_generation_controller import router as cag_router
from controllers.user_controller import router as user_router
from controllers.conversation_controller import router as conversation_router
from controllers.health_controller import router as health_router
from configs.mongo_config import mongodb, setup_legacy_clients

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

app = FastAPI(
    title="LearnAware AI Services",
    description="An API for the LearnAware AI Services",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup and shutdown events
@app.on_event("startup")
async def startup_db_client():
    """Initialize the database connection pool on application startup"""
    logger.info("Application starting up...")
    
    # Initialize MongoDB connection
    if mongodb.initialize():
        # Setup legacy client variables for backward compatibility
        setup_legacy_clients()
        logger.info("MongoDB connection pool initialized successfully")
    else:
        logger.warning("Failed to initialize MongoDB connection pool. Some features may not work properly.")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close the database connection on application shutdown"""
    logger.info("Application shutting down...")
    mongodb.close()
    logger.info("Closed all connections")

# Include routers
app.include_router(
    socratic_tutor_router, prefix="/api/v1/socratic-tutor", tags=["Socratic Tutor"]
)

app.include_router(
    cag_router,
    prefix="/api/v1/cag",
    tags=["Cached Augmented Generation"],
)

app.include_router(user_router, prefix="/api/v1/auth", tags=["User Authentication"])

app.include_router(
    conversation_router, prefix="/api/v1/conversations", tags=["Conversations"]
)

app.include_router(health_router, prefix="/api/v1/health", tags=["Health"])


@app.get("/")
def root():
    return {"message": "Welcome to the Socratic Tutor API!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
