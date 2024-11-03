# services/logic/inventory_logic.py
from models.dto import InventoryDTO, InventoryItemDTO
import json
import os


def load_inventory_data():
	with open('inventory.json', 'r') as f:
		data = json.load(f)
	return data['inventario']


def get_inventory():
	inventory_data = load_inventory_data()
	productos = [
		InventoryItemDTO(
			id_producto=item['id_producto'],
			nombre=item['nombre_producto'],
			marca=item['marca'],
			cantidad=item['cantidad_actual'],
			precio_compra=item['precio_compra'],
			precio_venta=item['precio_venta'],
			imagen=item['imagen'],
			canjeable=item['canjeable']
		)
		for item in inventory_data
	]
	return InventoryDTO(productos=productos)

def save_inventory_data(inventory):
	data = {'inventario': inventory}
	with open('inventory.json', 'w') as f:
		json.dump(data, f, indent=2)