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
	id_producto: int
	nombre: str
	marca: str
	cantidad: int
	precio_compra: str
	precio_venta: str
	imagen: str
	canjeable: bool

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
