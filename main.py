import pandas as pd
import toml
import sys
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager
from loguru import logger
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from db.db import get_db

from route import seed_data, poll_files, tag
from utils.utils import load_config

scheduler = AsyncIOScheduler()

@asynccontextmanager
async def lifespan(app: FastAPI):
    poll_rate: int = load_config().get('poll_rate')
    logger.info(f'Starting file-polling-service with poll rate of {poll_rate} seconds')

    scheduler.add_job(func=poll_files.poll_files, trigger='interval', seconds=poll_rate)
    scheduler.start()
    yield

app = FastAPI(lifespan=lifespan)


@app.put('/adjust/rate/{new_rate}')
async def update_poll_rate(new_rate: int):
    logger.info(f'Updating poll rate to {new_rate} seconds')
    job_id = next((job.id for job in scheduler.get_jobs()))
    scheduler.reschedule_job(job_id=job_id, trigger='interval', seconds=new_rate)


app.include_router(poll_files.router)

app.include_router(seed_data.router)
app.include_router(tag.router)







