from pydantic import BaseModel
from typing import List, Optional


class ResponseDTO(BaseModel):
	response: str


class SaleDTO(BaseModel):
	producto: str
	cantidad: int
	cliente: Optional[str]
	fecha: str


class InventoryItemDTO(BaseModel):
	nombre: str
	cantidad: int


class InventoryDTO(BaseModel):
	productos: List[InventoryItemDTO]


class OrderItemDTO(BaseModel):
	nombre: str
	cantidad: int
	catalogo_numero: Optional[int]


class OrderDTO(BaseModel):
	productos: List[OrderItemDTO]


class ExchangeDTO(BaseModel):
	producto: str
	cantidad: int
