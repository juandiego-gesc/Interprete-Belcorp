# util.py
import os
from dotenv import load_dotenv, find_dotenv
import google.generativeai as palm
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

load_dotenv(find_dotenv())


def get_chat_response(system_prompt, user_prompt):
	llm_type = os.environ.get('LLM_TYPE', 'google')
	if llm_type == 'google':
		return get_google_response(system_prompt, user_prompt)
	else:
		# Puedes mantener la opción de OpenAI si lo deseas
		return get_openai_response(system_prompt, user_prompt)


def get_google_response(system_prompt, user_prompt):
	api_key = os.environ.get('GOOGLE_API_KEY')
	palm.configure(api_key=api_key)

	# Combina el prompt del sistema y del usuario
	prompt = f"{system_prompt}\n\n{user_prompt}"

	try:
		model = palm.GenerativeModel("gemini-1.5-flash")
		response = model.generate_content(
			prompt
		)

		if response and hasattr(response, 'result'):
			return response.result
		else:
			return "No se obtuvo una respuesta del modelo."
	except Exception as e:
		return f"Ocurrió un error al obtener la respuesta del modelo: {e}"


def get_openai_response(system_prompt, user_prompt, model="gpt-3.5-turbo", temperature=0):
	chat = ChatOpenAI(model_name=model, temperature=temperature)
	messages = [
		SystemMessage(content=system_prompt),
		HumanMessage(content=user_prompt)
	]
	response = chat(messages)
	print(response)
	return response.content
