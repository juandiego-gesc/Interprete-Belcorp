from models.dto import InventoryDTO

async def get_inventory():
	# Datos de inventario simulados
	inventory_data = {
		"productos": [
			{"nombre": "labial rojo", "cantidad": 10},
			{"nombre": "perfume floral", "cantidad": 5},
			{"nombre": "crema hidratante", "cantidad": 8}
		]
	}
	inventory_dto = InventoryDTO(**inventory_data)
	return inventory_dto
