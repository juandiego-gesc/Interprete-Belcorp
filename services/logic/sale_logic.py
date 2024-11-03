# services/logic/sale_logic.py

from models.dto import SaleDTO
from .inventory_logic import load_inventory_data, save_inventory_data

def register_sale(sale_dto: SaleDTO):
	# Cargar inventario
	inventory = load_inventory_data()
	# Inicializar mensaje_inventario
	mensaje_inventario = ""
	# Buscar el producto
	for item in inventory:
		if item['nombre_producto'].lower() == sale_dto.producto.lower():
			cantidad_disponible = item['cantidad_actual']
			cantidad_vender = sale_dto.cantidad
			if cantidad_disponible >= cantidad_vender:
				# Actualizar cantidad
				item['cantidad_actual'] -= cantidad_vender
				cantidad_restante = item['cantidad_actual']
				mensaje_inventario = f"Inventario restante de {sale_dto.producto}: {cantidad_restante} unidades."
				success = True
			else:
				# Vender lo que hay y notificar la cantidad faltante
				cantidad_vendida = cantidad_disponible
				faltante = cantidad_vender - cantidad_disponible
				item['cantidad_actual'] = 0
				mensaje_inventario = (
					f"Se vendieron {cantidad_vendida} unidades de {sale_dto.producto}. "
					f"No hay suficiente inventario. Faltan {faltante} unidades que debes pedir."
				)
				success = True  # Si deseas considerar esto como éxito
				sale_dto.cantidad = cantidad_vendida  # Actualizar la cantidad vendida realmente
			break
	else:
		print("Producto no encontrado en el inventario.")
		return False, "Producto no encontrado en el inventario."  # Retornar una tupla aquí
	# Guardar inventario actualizado
	save_inventory_data(inventory)
	print(f"Venta registrada: {sale_dto.cantidad} unidades de {sale_dto.producto}.")
	return success, mensaje_inventario  # Retornar una tupla aquí
