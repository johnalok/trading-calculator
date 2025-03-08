import logging
from fastapi import FastAPI

# Set up logging to console and file
logging.basicConfig(
    level=logging.DEBUG,  # Capture all logs from DEBUG level and above
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log", mode='w'),  # Log to file (overwrite on each restart)
        logging.StreamHandler()  # Log to console
    ]
)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
async def test_logging():
    logger.info("This is an info log from /test-logging endpoint.")
    logger.debug("This is a debug log from /test-logging endpoint.")
    return {"message": "Check the logs for the test!"}
