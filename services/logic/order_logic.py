# services/logic/order_logic.py
from models.dto import OrderDTO
from .inventory_logic import load_inventory_data

def add_to_cart(order_dto: OrderDTO):
	# Aquí puedes simular agregar al carrito
	print(f"Productos agregados al carrito:")
	for item in order_dto.productos:
		print(f"- {item.cantidad} x {item.nombre}")
	# No es necesario actualizar el inventario en este punto
	return True
