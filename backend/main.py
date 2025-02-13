from fastapi import FastAPI

app = FastAPI()  # This is the main FastAPI app instance

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
