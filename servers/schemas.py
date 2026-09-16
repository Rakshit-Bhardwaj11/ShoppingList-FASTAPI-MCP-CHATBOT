from typing import Optional,List
from datetime import datetime
from pydantic import BaseModel,Field

#ShoppingList pydantic classes
class ShoppingListBase(BaseModel):
    name:str=Field(...,min_length=1,max_length=255,description='Name of list')
    description: str = Field(..., description="Optional description of shopping list")

class ShoppingListCreate(ShoppingListBase):
    pass

class ShoppingListUpdate(BaseModel):
    name:Optional[str]=Field(None,min_length=1,max_length=255)
    description:Optional[str]=None

class ShoppingListResponse(ShoppingListBase):
    id:int=Field(...,description='id of the shopping list')
    created_at:datetime=Field(...,description='The date at which list was created')
    updated_at:datetime=Field(...,description='The date at which list was updated')

    class Config:
        from_attributes=True

#Items pydantic classes

class ShoppingItemBase(BaseModel):
    name:str=Field(...,min_length=1,max_length=255,description='the name of the product')
    quantity:int=Field(1,ge=1,description='the quantity of the product brought')
    unit:Optional[str]=Field(None,max_length=50,description='Unit of measurement (e.g., kg, pieces)')
    notes:Optional[str]=Field(None,description='Enter some optional notes for the item')
    is_completed:bool=Field(default=False,description='Whether the order is completed or not')

class ShoppingItemCreate(ShoppingItemBase):
    shopping_list_id:int=Field(...,description='Enter the id of the shopping list where the product needs to be added')

class ShoppingItemUpdate(BaseModel):
    name:Optional[str]=Field(None,min_length=1,max_length=255)
    quantity:Optional[int]=Field(None,ge=1)
    unit:Optional[str]=Field(None,max_length=50)
    notes:Optional[str]=Field(None)
    is_completed:Optional[bool]=Field(None)

class ShoppingItemResponse(ShoppingItemBase):
    id:int
    created_at:datetime
    updated_at: datetime
    shopping_list_id:int

    class Config:

        from_attributes=True

#Combined response pydantic class

class ShoppingListWithItems(ShoppingListResponse):
    items: List[ShoppingItemResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True

        