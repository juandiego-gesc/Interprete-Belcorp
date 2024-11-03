# services/formatters/inventory_formatter.py
from services.logic.inventory_logic import get_inventory
from util import get_chat_response


# def handle_inventory_message(input_text):
# 	# Obtener el inventario desde la lógica
# 	inventory_dto = get_inventory()
# 	# Generar respuesta al usuario
# 	inventory_list = "\n".join([f"- {item.nombre}: {item.cantidad} unidades" for item in inventory_dto.productos])
# 	system_prompt = "Eres un asistente que ayuda a las consultoras de Belcorp."
# 	user_prompt = f"""
# 					Informa a la consultora sobre su inventario actual:
#
# 					{inventory_list}
#
# 					El mensaje debe ser claro y amigable.
# 					Respuesta:"""
#
# 	response = get_chat_response(system_prompt, user_prompt)
# 	return response.strip()

def handle_inventory_message(input_text):
	# Obtener el inventario desde la lógica
	inventory_dto = get_inventory()
	# Generar respuesta al usuario
	inventory_list = "\n".join([f"- {item.nombre}: {item.cantidad} unidades" for item in inventory_dto.productos])
	system_prompt = "Eres un asistente que ayuda a las consultoras de Belcorp."
	user_prompt = f"""
					Informa a la consultora sobre su inventario actual:
					
					{inventory_list}
					
					El mensaje debe ser claro y amigable.
					Respuesta:"""

	response = get_chat_response(system_prompt, user_prompt)
	# Construir el diccionario con 'texto' y 'productos'
	result = {
		"texto": response.strip(),
		"productos": [item.dict() for item in inventory_dto.productos]
	}
	return result

def handle_specific_inventory_message(input_text):
	# Cargar inventario y extraer nombres de productos
	inventory = load_inventory_data()
	product_names = [item['nombre_producto'] for item in inventory]
	product_names_str = ", ".join(f'"{name}"' for name in product_names)

	# Extraer el nombre del producto específico utilizando ChatGPT
	system_prompt = "Eres un asistente que identifica productos en mensajes de texto."
	user_prompt = f"""
Analiza el siguiente mensaje y extrae el nombre del producto que el usuario desea consultar.
Debes utilizar el nombre de producto más cercano de la lista de productos disponibles.

Los productos disponibles son: {product_names_str}

Mensaje: "{input_text}"

Proporciona la respuesta en formato JSON, por ejemplo:
{{
    "producto": "Máscara de Pestañas"
}}

Respuesta:"""
	response = get_chat_response(system_prompt, user_prompt)
	# Convertir la respuesta a un diccionario
	try:
		product_data = json.loads(response)
		producto = product_data.get("producto")

		# Buscar el producto en el inventario
		for item in inventory:
			if item['nombre_producto'].lower() == producto.lower():
				# Construir el mensaje con la información del producto
				mensaje = f"Información del producto '{item['nombre_producto']}':\n" \
				          f"- Marca: {item['marca']}\n" \
				          f"- Cantidad disponible: {item['cantidad_actual']} unidades\n" \
				          f"- Precio de compra: {item['precio_compra']}\n" \
				          f"- Precio de venta: {item['precio_venta']}\n" \
				          f"- Disponible para canje: {'Sí' if item['canjeable'] else 'No'}"
				return mensaje
		else:
			# Si el producto no se encuentra en el inventario
			return f"El producto '{producto}' no se encuentra en el inventario."
	except json.JSONDecodeError:
		return "No pude entender tu solicitud. Por favor, verifica la información."
	except Exception as e:
		print(f"Ocurrió un error: {e}")
		return "Ocurrió un error al procesar tu solicitud. Por favor, intenta nuevamente."