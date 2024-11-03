from models.dto import OrderDTO
from util import get_chat_response

async def format_order_response(order_dto: OrderDTO):
	product_list = "\n".join([f"- {item.cantidad} x {item.nombre} (Catálogo #{item.catalogo_numero})" for item in order_dto.productos])
	system_prompt = """Eres un asistente que ayuda a las consultoras de Belcorp."""
	user_prompt = f"""
Genera un mensaje confirmando que los siguientes productos han sido añadidos al carrito:

{product_list}

El mensaje debe ser entusiasta y brindar información sobre el siguiente paso.
Respuesta:"""
	response = get_chat_response(system_prompt, user_prompt)
	return response.strip()
