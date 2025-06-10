from fastapi import FastAPI

from app.handlers import router as general_router


app = FastAPI()


app.include_router(general_router)


@app.get("/")
def read_root():
    return {"Index": "Index.html"}
