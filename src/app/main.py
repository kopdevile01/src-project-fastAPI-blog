from fastapi import FastAPI

app = FastAPI(title="FastAPI Blog API")

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI blog API"}