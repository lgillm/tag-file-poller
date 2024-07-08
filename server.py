import uvicorn
from multiprocessing import cpu_count, freeze_support
import fastapi
from fastapi import FastAPI
import signal
from loguru import logger
import asyncio
from utils.utils import load_config
from datetime import datetime
import sys
import pyodbc
import databases


config = load_config()
DEFAULT_PORT = 5003


def init_logging() -> None:
    log_dir = 'logs'
    log_day = datetime.strftime(datetime.now(), "%Y-%m-%d")
    logger.add(f"{log_dir}\\app_{log_day}.log", format="{name} {message}", rotation="00:00")


def start_server(host="0.0.0.0",
                 port=DEFAULT_PORT,
                 num_workers=1,
                 loop="asyncio",
                 reload=False):
    uvicorn.run("main:app",
                host=host,
                port=port,
                workers=num_workers,
                loop=loop,
                reload=reload)


def shutdown(signum, frame):
    logger.info("Shutting down gracefully...")
    sys.exit(0)


if __name__ == "__main__":
    freeze_support()  # Needed for pyinstaller for multiprocessing on WindowsOS
    init_logging()
    signal.signal(signal.SIGINT, shutdown)
    port = config.get("port", DEFAULT_PORT)
    logger.info(f'Starting csv-polling-service at port {port}')
    num_workers = 1#int(cpu_count() * 0.75)
    start_server(num_workers=num_workers, port=port)
