import uuid
from enum import Enum
from pydantic import BaseModel, ConfigDict

class SauceSpicienessEnum(str, Enum):
    mild ='mild'
    unmild = 'unmild'
    unhealthy = 'unhealthy'

class SauceBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    price: float
    description: str
    spicieness: SauceSpicienessEnum


class SauceCreateSchema(SauceBaseSchema):
    stock: int


class SauceSchema(SauceCreateSchema):
    id: uuid.UUID


class SauceListItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    name: str
    price: float
    description: str
    spicieness: SauceSpicienessEnum


