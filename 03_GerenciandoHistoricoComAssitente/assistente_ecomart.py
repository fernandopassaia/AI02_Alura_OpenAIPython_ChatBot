from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from selecionar_persona import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# preciso adicionar o gpt4 preview, por que o normal não aceita ler e devolver vários arquivos
modelo = "gpt-4-1106-preview"
contexto = carrega("dados/ecomart.txt")


def criar_thread():
    return cliente.beta.threads.create()


def criar_assistente():
    assistente = cliente.beta.assistants.create(
        name="Atendente EcoMart",
        instructions=f"""
            Você é um chatbot de atendimento a clientes de um e-commerce.
            Além disso, adote a persona abaixo para responder ao cliente.
            
            ## Contexto
            {contexto}
            
            ## Persona
            
            {personas["neutro"]}
        """,
        model=modelo,
    )
    return assistente
