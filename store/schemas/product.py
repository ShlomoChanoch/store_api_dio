from decimal import Decimal
from typing import Annotated, Optional
from datetime import datetime
from bson import Decimal128
from pydantic import AfterValidator, Field, BeforeValidator
from store.schemas.base import BaseSchemaMixin, OutSchema


PyDecimal = Annotated[
    Decimal, BeforeValidator(lambda v: v.to_decimal() if isinstance(v, Decimal128) else v)
]

class ProductBase(BaseSchemaMixin):
    name: str = Field(..., description="Product name")
    quantity: int = Field(..., description="Product quantity")
    price: PyDecimal = Field(..., description="Product price")
    status: bool = Field(..., description="Product status")


class ProductIn(ProductBase, BaseSchemaMixin):
    ...

class ProductOut(ProductIn, OutSchema):
    ...


def convert_decimal_128(v):
    return Decimal128(str(v))

Decimal_ = Annotated[Decimal, AfterValidator(convert_decimal_128)]

class ProductUpdate(BaseSchemaMixin):
    quantity: Optional[int] = Field(None, description="Product quantity")
    price: Optional[Decimal_] = Field(None, description="Product price")
    status: Optional[bool] = Field(None, description="Product status")
    updated_at: Optional[datetime] = Field(None, description="Product update time")


class ProductUpdateOut(ProductOut):
    ...
