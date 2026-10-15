from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from api.v1.api import api_router
from core.config import settings
from core.logger import logger

app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware bắt lỗi hệ thống và ghi log
@app.middleware("http")
async def exception_logging_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as exc:
        logger.exception(f"Lỗi Unhandled | {request.method} {request.url.path} | Error: {exc}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Lỗi nội bộ hệ thống. Vui lòng kiểm tra lại log server."},
        )

# Gắn toàn bộ router v1
app.include_router(api_router)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "app": settings.APP_NAME}