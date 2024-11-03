from models.dto import ExchangeDTO
from util import get_chat_response


async def register_exchange(exchange_request):
	input_text = exchange_request.get("message", "")
	# Aquí extraemos los detalles del producto para canje
	# Para el demo, usaremos datos fijos
	exchange_data = {
		"producto": "perfume floral",
		"cantidad": 2
	}
	exchange_dto = ExchangeDTO(**exchange_data)
	# Lógica para registrar el producto para canje (omitida en el demo)
	return exchange_dto
