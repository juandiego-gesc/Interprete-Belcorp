from models.dto import ExchangeDTO
from util import get_chat_response

async def format_exchange_response(exchange_dto: ExchangeDTO):
	system_prompt = """Eres un asistente que ayuda a las consultoras de Belcorp."""
	user_prompt = f"""
Genera un mensaje confirmando que el siguiente producto ha sido registrado para canje:

Producto: {exchange_dto.producto}
Cantidad: {exchange_dto.cantidad}

El mensaje debe ser cordial y explicar que será visible para otras consultoras.
Respuesta:"""
	response = get_chat_response(system_prompt, user_prompt)
	return response.strip()
