# services/formatters/sale_formatter.py
from models.dto import SaleDTO
from services.logic.sale_logic import register_sale
from services.logic.inventory_logic import load_inventory_data
from util import get_chat_response
import json
from datetime import datetime

def handle_sale_message(input_text):
	# Cargar inventario y extraer nombres de productos
	inventory = load_inventory_data()
	product_names = [item['nombre_producto'] for item in inventory]
	product_names_str = ", ".join(f'"{name}"' for name in product_names)

	# Extraer detalles de la venta utilizando ChatGPT
	system_prompt = "Eres un asistente que extrae detalles de ventas de mensajes de texto."
	user_prompt = f"""
		Analiza el siguiente mensaje y extrae los detalles de la venta en un formato estructurado.
		Debes identificar el producto y la cantidad.
		
		Los productos disponibles son: {product_names_str}
		
		Utiliza el nombre de producto más cercano de la lista de productos disponibles.
		
		Mensaje: "{input_text}"
		
		Proporciona la respuesta en formato JSON, por ejemplo:
		{{
		    "producto": "Máscara de Pestañas",
		    "cantidad": 3
		}}

Respuesta:"""
	response = get_chat_response(system_prompt, user_prompt)
	# Convertir la respuesta a un DTO
	try:
		sale_data = json.loads(response)
		producto = sale_data.get("producto")
		cantidad = int(sale_data.get("cantidad"))

		sale_dto = SaleDTO(
			producto=producto,
			cantidad=cantidad,
			cliente=None,
			fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		)

		# Llamar a la lógica
		success, mensaje_inventario = register_sale(sale_dto)
		# Generar respuesta al usuario
		if success:
			respuesta = f"¡Venta registrada! {sale_dto.cantidad} unidades de {sale_dto.producto}."
			if mensaje_inventario:
				respuesta += f" Nota: {mensaje_inventario}"
			return respuesta
		else:
			return "No se pudo registrar la venta. Por favor, verifica el producto."
	except json.JSONDecodeError:
		return "No pude entender los detalles de la venta. Por favor, verifica la información."
	except Exception as e:
		print(f"Ocurrió un error: {e}")
		return "Ocurrió un error al procesar tu venta. Por favor, intenta nuevamente."
