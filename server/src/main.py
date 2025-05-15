import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .utils.errors import register_all_errors
from .utils.middleware import register_middleware

from .auth.routes import auth_router
from .chat.routes import chat_router

version = "v1"

description = """An API for the LearnAware AI Services"""

version_prefix =f"/api/{version}"

app = FastAPI(
    title="LearnAware AI Services",
    description=description,
    version=version,
    license_info={"name": "MIT License", "url": "https://opensource.org/license/mit"},
        contact={
        "name": "tharoosha vihidun",
        "url": "https://github.com/tharooshavihidun",
        "email": "tharooshavihidun@gmail.com",
    },
)

register_all_errors(app)
register_middleware(app)

app.include_router(
    auth_router, prefix=f"{version_prefix}/auth", tags=["auth"])
app.include_router(
    chat_router, prefix=f"{version_prefix}/chat", tags=["chat"])

@app.get("/")
def root():
    return {"message": "Welcome to the Socratic Tutor API!"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
