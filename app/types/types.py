from typing import TypedDict
import uuid

class UserUpdateData(TypedDict, total=False):
    username: str
    password_hash: str
    email: str

class SchoolUpdateData(TypedDict, total=False):
    name: str
    address: str

class ProductUpdateData(TypedDict, total=False):
    name: str
    price: float

class OrderUpdateData(TypedDict, total=False):
    product_id: uuid.UUID
    amount: int

