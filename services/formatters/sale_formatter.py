from models.dto import SaleDTO
from util import get_chat_response

async def format_sale_response(sale_dto: SaleDTO):
	system_prompt = """Eres un asistente que ayuda a las consultoras de Belcorp."""
	user_prompt = f"""
Genera un mensaje confirmando el registro de la siguiente venta:

Producto: {sale_dto.producto}
Cantidad: {sale_dto.cantidad}
Cliente: {sale_dto.cliente if sale_dto.cliente else 'No especificado'}
Fecha: {sale_dto.fecha}

El mensaje debe ser amigable y motivador.
Respuesta:"""
	response = get_chat_response(system_prompt, user_prompt)
	return response.strip()
