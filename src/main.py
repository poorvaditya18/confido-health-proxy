import sys
import logging
from fastapi import FastAPI
from contextlib import asynccontextmanager
from services.redis_service import RedisService
from configs.db_config import Database
from configs.config import Config
from controllers import routes
from configs.db_singleton import init_db

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("confido-ehr-proxy")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        RedisService()
        init_db() 
        logger.info("database connected")
    except Exception as e:
        logger.error("Failed to initialize server. err: %s", e)
        sys.exit(f"cannot start server because of unexpected error.")
        
    yield
    logger.info("shutting down Confido EHR Proxy API...")

app = FastAPI(title="confido-ehr-proxy", lifespan=lifespan)
app.include_router(routes.router)

@app.get("/health")
def health():
    return {"status": "ok"}