# services/formatters/exchange_formatter.py
from models.dto import ExchangeDTO
from services.logic.exchange_logic import register_exchange
from services.logic.inventory_logic import load_inventory_data
from util import get_chat_response
import json

def handle_exchange_message(input_text):
	# Cargar inventario y extraer nombres de productos
	inventory = load_inventory_data()
	product_names = [item['nombre_producto'] for item in inventory]
	product_names_str = ", ".join(f'"{name}"' for name in product_names)

	# Extraer detalles del producto para canje utilizando ChatGPT
	system_prompt = "Eres un asistente que extrae detalles de productos sobrantes para canje."
	user_prompt = f"""
    Analiza el siguiente mensaje y extrae los detalles del producto sobrante que la consultora quiere ofrecer para canje.
    Debes identificar el producto y la cantidad.

    Los productos disponibles son: {product_names_str}

    Utiliza el nombre de producto más cercano de la lista de productos disponibles.

    Mensaje: "{input_text}"

    Proporciona la respuesta en formato JSON, por ejemplo:
    {{
        "producto": "Máscara de Pestañas",
        "cantidad": 2
    }}

    Respuesta:"""
	response = get_chat_response(system_prompt, user_prompt)
	# Convertir la respuesta a un DTO
	try:
		exchange_data = json.loads(response)
		exchange_dto = ExchangeDTO(
			producto=exchange_data.get("producto"),
			cantidad=int(exchange_data.get("cantidad"))
		)
		# Llamar a la lógica
		success, mensaje = register_exchange(exchange_dto)
		# Generar respuesta al usuario
		if success:
			system_prompt = "Eres un asistente que ayuda a las consultoras de Belcorp."
			user_prompt = f"""
    Confirma que el siguiente producto ha sido registrado para canje:

    Producto: {exchange_dto.producto}
    Cantidad: {exchange_dto.cantidad}

    El mensaje debe ser cordial y explicar que estará disponible para otras consultoras.
    Respuesta:"""
			confirmation_response = get_chat_response(system_prompt, user_prompt)
			return confirmation_response.strip()
		else:
			# Si no se pudo registrar, devolver el mensaje de error
			return f"No se pudo registrar el producto para canje. {mensaje}"
	except json.JSONDecodeError:
		return "No pude entender los detalles del producto para canje. Por favor, verifica la información."
