from contextlib import asynccontextmanager

from fastapi import FastAPI

from api import router
from core import settings
from core.logger import logger
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

app.include_router(router)

# class CustomUvicornWorker(UvicornWorker):
#     CONFIG_KWARGS = {
#         "loop": "uvloop",
#         "http": "h11",
#         "log_config": LOGGING,
#         "log_level": getattr(logging, settings.logger_logging_lvl),
#     }
