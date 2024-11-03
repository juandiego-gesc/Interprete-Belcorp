from models.dto import InventoryDTO
from util import get_chat_response


async def format_inventory_response(inventory_dto: InventoryDTO):
	inventory_list = "\n".join([f"- {item.nombre}: {item.cantidad} unidades" for item in inventory_dto.productos])
	system_prompt = """Eres un asistente que ayuda a las consultoras de Belcorp."""
	user_prompt = f"""
Genera un mensaje informando a la consultora sobre su inventario actual:

{inventory_list}

El mensaje debe ser claro y amigable.
Respuesta:"""
	response = get_chat_response(system_prompt, user_prompt)
	return response.strip()
