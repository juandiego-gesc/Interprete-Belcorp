# services/logic/exchange_logic.py
from models.dto import ExchangeDTO
from .inventory_logic import load_inventory_data, save_inventory_data

def register_exchange(exchange_dto: ExchangeDTO):
	inventory = load_inventory_data()
	for item in inventory:
		if item['nombre_producto'].lower() == exchange_dto.producto.lower():
			# Actualizar canjeable y cantidad
			item['canjeable'] = True
			item['cantidad_actual'] += exchange_dto.cantidad
			# Guardar inventario actualizado
			save_inventory_data(inventory)
			mensaje = f"{exchange_dto.cantidad} unidades de {exchange_dto.producto} han sido registradas para canje."
			return True, mensaje
	else:
		mensaje = "El producto no se encuentra en el inventario."
		return False, mensaje