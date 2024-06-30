from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastui import prebuilt_html
from starlette.responses import HTMLResponse

from api.v1.auth import auth_router
from api.v1.uploads import uploads_router
from pages.routers import router as pages_router
from core import settings
from core.logger import logger
from services.postgres import sessionmanager
from httpx import AsyncClient
from fastapi.staticfiles import StaticFiles

@asynccontextmanager
async def lifespan(app: FastAPI):
    sessionmanager.init(settings.get_db_url())
    logger.info("service is ready to startup")
    # async with AsyncClient() as client:
    #     app_.state.httpx_client = client
    yield
    await sessionmanager.close()
    logger.info("service is ready to shutdown")


# @asynccontextmanager
# async def lifespan(app_: FastAPI):
#     async with AsyncClient() as client:
#         app_.state.httpx_client = client
#         yield

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

# class CustomUvicornWorker(UvicornWorker):
#     CONFIG_KWARGS = {
#         "loop": "uvloop",
#         "http": "h11",
#         "log_config": LOGGING,
#         "log_level": getattr(logging, settings.logger_logging_lvl),
#     }


@app.get('/demo/{path:path}')
async def html_landing() -> HTMLResponse:
    return HTMLResponse(prebuilt_html(title='FastUI Demo'))
