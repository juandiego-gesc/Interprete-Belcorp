# services/formatters/order_formatter.py
from models.dto import OrderDTO, OrderItemDTO
from services.logic.order_logic import add_to_cart
from util import get_chat_response

def handle_order_message(input_text):
	# Extraer detalles del pedido utilizando ChatGPT
	system_prompt = "Eres un asistente que extrae detalles de pedidos de mensajes de texto."
	user_prompt = f"""
					Analiza el siguiente mensaje y extrae los detalles del pedido en un formato estructurado.
					Debes identificar los productos, las cantidades y los números de catálogo si están disponibles.
					
					Mensaje: "{input_text}"
					
					Proporciona la respuesta en formato JSON, por ejemplo:
					{{
					    "productos": [
					        {{"nombre": "crema hidratante", "cantidad": 5, "catalogo_numero": 123}},
					        {{"nombre": "loción corporal", "cantidad": 2, "catalogo_numero": 456}}
					    ]
					}}
					
					Respuesta:"""
	response = get_chat_response(system_prompt, user_prompt)
	# Convertir la respuesta a un DTO
	import json
	try:
		order_data = json.loads(response)
		order_items = [
			OrderItemDTO(
				nombre=item.get("nombre"),
				cantidad=item.get("cantidad"),
				catalogo_numero=item.get("catalogo_numero")
			)
			for item in order_data.get("productos", [])
		]
		order_dto = OrderDTO(productos=order_items)
		# Llamar a la lógica
		add_to_cart(order_dto)
		# Generar respuesta al usuario
		product_list = "\n".join([f"- {item.cantidad} x {item.nombre} (Catálogo #{item.catalogo_numero})" for item in order_dto.productos])
		system_prompt = "Eres un asistente que ayuda a las consultoras de Belcorp."
		user_prompt = f"""
						Confirma que los siguientes productos han sido añadidos al carrito:
						
						{product_list}
						
						El mensaje debe ser entusiasta y brindar información sobre el siguiente paso.
						Respuesta:"""
		confirmation_response = get_chat_response(system_prompt, user_prompt)
		return confirmation_response.strip()
	except json.JSONDecodeError:
		return "No pude entender los detalles del pedido. Por favor, verifica la información."
