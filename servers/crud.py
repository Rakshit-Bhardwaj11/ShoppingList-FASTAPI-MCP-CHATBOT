from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional,List
from .models import ShoppingItem,ShoppingList
from .schemas import ShoppingItemCreate,ShoppingItemUpdate,ShoppingListCreate,ShoppingListUpdate

#Shopping List CRUD Operations
async def create_shopping_list(db: AsyncSession, shopping_list: ShoppingListCreate)->ShoppingList:
    shopping_list_db=ShoppingList(**shopping_list.model_dump())
    db.add(shopping_list_db)
    await db.commit()
    await db.refresh(shopping_list_db)
    return shopping_list_db

async def get_shopping_list(db: AsyncSession, shopping_list_id:int)-> Optional[ShoppingList]:
    result = await db.execute(select(ShoppingList).where(ShoppingList.id == shopping_list_id) )
    return result.scalars().first()

async def get_shopping_lists(db: AsyncSession,skip:int=0,limit:int=100)->List[ShoppingList]:
    results=await db.execute(select(ShoppingList).offset(skip).limit(limit))
    return results.scalars().all()

async def update_shopping_list(db: AsyncSession,shopping_list_id:int, shopping_list:ShoppingListUpdate)->ShoppingList:
    result= await db.execute(select(ShoppingList).where(ShoppingList.id==shopping_list_id))
    db_shopping_list=result.scalars().first()

    if db_shopping_list:
        updated_data=shopping_list.model_dump(exclude_unset=True)
        for key,value in updated_data.items():
            setattr(db_shopping_list,key,value)
        await db.commit()
        await db.refresh(db_shopping_list)
        return db_shopping_list
    return None 

async def delete_shopping_list(db: AsyncSession,shopping_list_id:int)->bool:
    result= await db.execute(select(ShoppingList).where(ShoppingList.id==shopping_list_id))
    db_shopping_list=result.scalars().first()
    if db_shopping_list:
        await db.delete(db_shopping_list)
        await db.commit()
        return True
    return False

#Shopping Items crud Operations

async def create_shopping_item(db:AsyncSession,shopping_item:ShoppingItemCreate)->ShoppingItem:
    db_shopping_item=ShoppingItem(**shopping_item.model_dump())
    db.add(db_shopping_item)
    await db.commit()
    await db.refresh(db_shopping_item)
    return db_shopping_item

async def get_shopping_item(db:AsyncSession,shopping_item_id:int)->Optional[ShoppingItem]:
    result= await db.execute(select(ShoppingItem).where(ShoppingItem.id==shopping_item_id))
    return result.scalars().first()

async def get_shopping_items(db:AsyncSession,shopping_list_id:Optional[int]=None,skip:int=0,limit:int=100)->List[ShoppingItem]:
    query=select(ShoppingItem).offset(skip).limit(limit)
    if shopping_list_id:
        query=query.filter(ShoppingItem.shopping_list_id==shopping_list_id)
    results=await db.execute(query)
    return results.scalars().all()

async def update_shopping_item(db:AsyncSession,item_id:int,shopping_item:ShoppingItemUpdate)->ShoppingItem:
    result=await db.execute(select(ShoppingItem).where(ShoppingItem.id==item_id))
    db_shopping_item=result.scalars().first()
    if db_shopping_item:
        updated_item=shopping_item.model_dump(exclude_unset=True)
        for key,value in updated_item.items():
            setattr(db_shopping_item,key,value)
        await db.commit()
        await db.refresh(db_shopping_item)
    return db_shopping_item

async def delete_shopping_item(db:AsyncSession,item_id:int)->bool:
    result=await db.execute(select(ShoppingItem).filter(ShoppingItem.id==item_id))
    db_shopping_item=result.scalars().first()
    if db_shopping_item:
        await db.delete(db_shopping_item)
        await db.commit()
        return True
    return False


async def toggle_item_completion(db:AsyncSession,item_id:int)->Optional[ShoppingItem]:
    results= await db.execute(select(ShoppingItem).where(ShoppingItem.id==item_id))
    db_shopping_item= results.scalars().first()

    if db_shopping_item:
        db_shopping_item.is_completed = not db_shopping_item.is_completed
        await db.commit()
        await db.refresh(db_shopping_item)
        return db_shopping_item
    return None