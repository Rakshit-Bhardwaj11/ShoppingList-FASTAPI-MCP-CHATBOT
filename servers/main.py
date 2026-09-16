from contextlib import asynccontextmanager
from fastapi import FastAPI,HTTPException,Depends
from typing import Annotated,List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_mcp import FastApiMCP

from .database import get_db,async_engine
from .models import Base
from .schemas import (ShoppingItemUpdate,ShoppingItemCreate,ShoppingItemResponse,ShoppingListUpdate,ShoppingListCreate,ShoppingListResponse,ShoppingListWithItems)

from .crud import (get_shopping_list,get_shopping_lists,create_shopping_list,delete_shopping_list,update_shopping_list,get_shopping_item,get_shopping_items,create_shopping_item,delete_shopping_item,update_shopping_item,toggle_item_completion)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await async_engine.dispose()

app = FastAPI(description='REST api for managing shopping lists',lifespan=lifespan)

db_dependency=Annotated[AsyncSession,Depends(get_db)]

@app.get("/")
async def home(): return {"message": "Welcome to the Shopping List API","docs": "/docs","status": "running"}

@app.post("/shopping-list/",response_model=ShoppingListResponse,operation_id='create_shopping_list',summary="Create a new shopping list")
async def create_list(shopping_list:ShoppingListCreate,db:db_dependency):
    "Create a new shopping lists"
    return await create_shopping_list(db=db,shopping_list=shopping_list)

@app.get("/shopping-lists/",response_model=List[ShoppingListResponse],operation_id="get_shopping_lists",summary="Get all the lists")
async def get_lists(db:db_dependency,skip:int=0,limit:int=100):
    "Get all the lists from the database with skips and limit"
    shopping_lists= await get_shopping_lists(db,skip=skip,limit=limit)
    return shopping_lists

@app.get("/shopping-list/{shopping_list_id}",response_model=ShoppingListWithItems,operation_id="get_shopping_list",description="Get the shopping list with the given shopping list id")
async def get_list(db:db_dependency,shopping_list_id:int):
    "Get the list with the given shopping_list_id"
    shopping_list= await get_shopping_list(db=db,shopping_list_id=shopping_list_id)
    if shopping_list is None:
        raise HTTPException(status_code=404,detail='shopping list not found')
    else:
        return shopping_list

@app.put("/shopping-list/{shopping_list_id}",response_model=ShoppingListResponse,operation_id='update_shopping_list',description="Update the shopping list")
async def update_list(db:db_dependency,shopping_list_id:int,shopping_list:ShoppingListUpdate):
    "Update the shopping list with given id and new list"
    updated_shopping_list= await update_shopping_list(db,shopping_list_id=shopping_list_id,shopping_list=shopping_list)
    if updated_shopping_list is None:
        raise HTTPException(status_code=404,detail='shopping list not found')
    else:
        return updated_shopping_list

@app.delete("/shopping-list/{shopping_list_id}",operation_id="delete_shopping_list",description="Delete the particular shopping list")
async def delete_list(db:db_dependency,shopping_list_id:int):
    "Delete the shopping list with given id and new list"
    success=await delete_shopping_list(db,shopping_list_id=shopping_list_id)
    if success is False:
        raise HTTPException(status_code=404,detail="shopping_list not found") 
    else:
        return{"message":"List is deleted"}

@app.post("/shopping-item/",response_model=ShoppingItemResponse,operation_id="create_shopping_item",description="create the given shopping item")
async def create_item(db:db_dependency,shopping_item:ShoppingItemCreate):
    "Create the given shopping item"
    shopping_lsit= await get_shopping_list(db,shopping_list_id=shopping_item.shopping_list_id)
    if not shopping_lsit:
        raise HTTPException(status_code=404,detail="Shopping list not found")
    else:
        return await create_shopping_item(db, shopping_item=shopping_item)

@app.get("/shopping-items/",response_model=List[ShoppingItemResponse],operation_id='get_shopping_items',description="Get all the shopping lists")
async def read_items(db:db_dependency,shopping_list_id:int,skip:int=0,limit:int=100):
    "Get all the shopping items from a shopping list"
    items=await get_shopping_items(db,shopping_list_id=shopping_list_id,skip=skip,limit=limit)
    return items

@app.get("/shopping-items/{item_id}",response_model=ShoppingItemResponse,operation_id="get_shopping_item",description="Get the item with the item id")
async def read_item(db:db_dependency,item_id:int):
    "et the item id with the given item id"
    item= await get_shopping_item(db,shopping_item_id=item_id)
    if item is None:
        raise HTTPException(status_code=404,detail="item not found")
    else:
        return item

@app.put("/shopping-items/{item_id}",response_model=ShoppingItemResponse,operation_id="update_item",description="Update the given shopping item ")
async def update_item(db:db_dependency,shopping_item:ShoppingItemUpdate,item_id:int):
    db_item= await update_shopping_item(db,item_id=item_id,shopping_item=shopping_item)
    if db_item is None:
        raise HTTPException(status_code=404,detail="item not found")
    else:
        return db_item

@app.delete("/shopping-items/{item_id}",operation_id="delete_item",description="Delete the given item")
async def delete_item(db:db_dependency,item_id:int):
    success=await delete_shopping_item(db,item_id=item_id)

    if success is False:
        raise HTTPException(status_code=404,detail="item not found")
    else:
        return {"message":"The item has been deleted"}

@app.patch("/shopping_items/{item_id}/toggle",response_model=ShoppingItemResponse,operation_id="toggle_item_completion",description="toggle the item update column")
async def toggle_item(db:db_dependency,item_id:int):
    "Toggle the updation of the transaction for the item"
    item_db= await toggle_item_completion(db,item_id=item_id)
    if item_db is None:
        raise HTTPException(status_code=404,detail="item not found")
    else:
        return item_db

mcp=FastApiMCP(app)
mcp.mount()
mcp.setup_server()