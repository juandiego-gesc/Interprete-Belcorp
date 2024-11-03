from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from tool_planner import user_input_handler
from models.dto import ResponseDTO
from services.logic.sale_logic import register_sale
from services.logic.inventory_logic import get_inventory
from services.logic.order_logic import add_to_cart
from services.logic.exchange_logic import register_exchange

app = FastAPI()


# Define los orígenes permitidos (en este caso, la URL de la app de React)
origins = [
    "http://localhost:8000",  # Cambia esto por el origen de tu app de React si es diferente
    "https://5418-201-221-122-178.ngrok-free.app/",
     "*"   # Cambia esto por el dominio de tu túnel ngrok
]

# Agrega el middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Permitir todos los headers
)



@app.post("/whatsapp_webhook")
async def whatsapp_webhook(request: Request):
    data = await request.json()
    message = data.get('message', '')
    response_text = user_input_handler(message)
    return {"response": response_text}


# Endpoints que retornan información cruda (DTOs)

@app.post("/register_sale")
async def endpoint_register_sale(sale_request: dict):
    sale_dto = await register_sale(sale_request)
    return sale_dto


@app.get("/get_inventory")
async def endpoint_get_inventory():
    inventory_dto = get_inventory()
    return inventory_dto


@app.post("/add_to_cart")
async def endpoint_add_to_cart(order_request: dict):
    order_dto = await add_to_cart(order_request)
    return order_dto


@app.post("/register_exchange")
async def endpoint_register_exchange(exchange_request: dict):
    exchange_dto = await register_exchange(exchange_request)
    return exchange_dto
