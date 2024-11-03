from datetime import datetime
from models.dto import SaleDTO
from util import get_chat_response

async def register_sale(sale_request):
	input_text = sale_request.get("message", "")
	# Aquí extraemos los detalles de la venta
	# Para el demo, usaremos datos fijos
	sale_data = {
		"producto": "labial rojo",
		"cantidad": 3,
		"cliente": "María",
		"fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	}
	sale_dto = SaleDTO(**sale_data)
	# Lógica para registrar la venta en el sistema (omitida en el demo)
	return sale_dto

