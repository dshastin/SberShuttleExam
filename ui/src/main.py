from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastui import prebuilt_html
from starlette.responses import HTMLResponse

from api.v1.auth import auth_router
from api.v1.uploads import uploads_router
from api.v1.users import users_router
from core import settings
from core.logger import logger
from pages.routers import router as pages_router
from services.postgres import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager.init(settings.get_db_url())
    logger.info("service is ready to startup")
    yield
    await sessionmanager.close()
    logger.info("service is ready to shutdown")


app = FastAPI(
    title=settings.project_name,
    docs_url="/api/openapi/",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth_router, prefix='/api')
app.include_router(uploads_router, prefix='/api')
app.include_router(pages_router, prefix='/pages')
app.include_router(users_router, prefix='/api')
