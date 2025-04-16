from fastapi import FastAPI
from app.handlers import router as general_router


app = FastAPI()


app.include_router(general_router)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/hello/")
def hello(name: str):
    name = name.strip().title()
    return {"message": f"Hello {name}"}


@app.get("/items/")
def list_items():
    return ["Item 1", "Item 2", "Item 3"]


@app.get("/items/{item_id}")
def get_tem_by_id(item_id: int):
    return {"item": {"id": item_id}}
