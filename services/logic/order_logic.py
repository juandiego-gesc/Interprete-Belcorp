from models.dto import OrderDTO
from util import get_chat_response


async def add_to_cart(order_request):
	input_text = order_request.get("message", "")
	# Aquí extraemos los detalles del pedido
	# Para el demo, usaremos datos fijos
	order_data = {
		"productos": [
			{"nombre": "crema hidratante", "cantidad": 5, "catalogo_numero": 123}
		]
	}
	order_dto = OrderDTO(**order_data)
	# Lógica para agregar al carrito (omitida en el demo)
	return order_dto
