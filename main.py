import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.app:app", host="0.0.0.0", port=8000, reload=True)














































# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel


# app = FastAPI()

# class Item(BaseModel):
#     text:str = None
#     is_done:bool = False

# items = []



# @app.get("/")
# def root():
#     return {"Hello": "World"}

# @app.post("/items")
# def create_item(item:Item):
#     items.append(item)
#     return items


# @app.get("/items")
# def list_items(limit:int=10,response_model=list[Item]):

#     return items[0:limit]


# @app.get("/items/{item_id}")
# def get_item(item_id:int,response_model=Item):
#     if item_id < len(items):
#         return items[item_id]
#     else:
#         raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
#     item = items[item_id]   
#     return item
