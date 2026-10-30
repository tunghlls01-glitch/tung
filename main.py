from fastapi import FastAPI, HTTPException, status
from db.database import Base, engine
from core.response import handler_http_exception
import models
from routers.auth_router import router as auth_routers
from routers.user_router import router as user_routers
from routers.project_router import router as project_routers
from routers.member_router import router as member_routers
from routers.task_router import router as task_routers
from routers.comment_router import router as comment_routers
from routers.attachment_router import router as attachment_routers

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RESEARCH GROUP MANAGEMENT API",
    version="1.0.0"
)

app.add_exception_handler(HTTPException, handler_http_exception)

app.include_router(auth_routers)
app.include_router(user_routers)
app.include_router(project_routers)
app.include_router(member_routers)
app.include_router(task_routers)
app.include_router(comment_routers)
app.include_router(attachment_routers)

@app.get("/health", tags=["CHECK API"])
def health_check():
    return {
        "success": True,
        "status_code":status.HTTP_200_OK,
        "message": "Dịch vụ đang hoạt động bình thường và ổn định.",
        "data": None
    }

