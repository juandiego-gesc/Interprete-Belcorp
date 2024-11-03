from services.logic.sale_logic import register_sale
from services.logic.inventory_logic import get_inventory
from services.logic.order_logic import add_to_cart
from services.logic.exchange_logic import register_exchange
from services.formatters.sale_formatter import format_sale_response
from services.formatters.inventory_formatter import format_inventory_response
from services.formatters.order_formatter import format_order_response
from services.formatters.exchange_formatter import format_exchange_response
from util import get_chat_response


async def tool_selection(input_text):
	system_prompt = """Eres un asistente virtual para las consultoras de Belcorp."""
	user_prompt = f"""
Necesitas actuar como un recomendador de herramientas según los mensajes de las consultoras.
Analiza el mensaje del usuario y elige una de las siguientes herramientas para ayudar a procesar la solicitud.
Tu respuesta debe ser solo el nombre de la herramienta, sin ninguna otra palabra o símbolo.

Las herramientas son:

- Sale_Service: Cuando la consultora quiere registrar una venta. Por ejemplo, "Vendí 3 labiales rojos a una clienta".
- Inventory_Service: Cuando la consultora quiere revisar su inventario. Por ejemplo, "¿Cuánto inventario tengo disponible?".
- Order_Service: Cuando la consultora quiere hacer un pedido de productos. Por ejemplo, "Necesito pedir 5 cremas hidratantes".
- Exchange_Service: Cuando la consultora quiere registrar productos sobrantes para canje. Por ejemplo, "Me sobraron 2 perfumes, márcalos disponibles para canje".
- No_Tool: Cuando el mensaje no corresponde a ninguna de las acciones anteriores.

Aquí está el mensaje del usuario: "{input_text}"
Tu respuesta:"""
	response = get_chat_response(system_prompt, user_prompt)
	return response.strip()


async def user_input_handler(input_text):
	tool = await tool_selection(input_text)
	print(f"Herramienta seleccionada: {tool}")
	if tool == "Sale_Service":
		sale_dto = await register_sale({"message": input_text})
		response_text = await format_sale_response(sale_dto)
		return response_text
	elif tool == "Inventory_Service":
		inventory_dto = await get_inventory()
		response_text = await format_inventory_response(inventory_dto)
		return response_text
	elif tool == "Order_Service":
		order_dto = await add_to_cart({"message": input_text})
		response_text = await format_order_response(order_dto)
		return response_text
	elif tool == "Exchange_Service":
		exchange_dto = await register_exchange({"message": input_text})
		response_text = await format_exchange_response(exchange_dto)
		return response_text
	else:
		response = get_chat_response("Eres un asistente virtual para las consultoras de Belcorp. responde estas "
		                             "preguntas generales, solo responde con maximo 20 palabras",
		                             input_text)
		return response
