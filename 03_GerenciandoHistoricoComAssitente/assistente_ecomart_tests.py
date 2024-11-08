from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *
from selecionar_persona import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4o-mini"
contexto = carrega("dados/ecomart.txt")

assistente = cliente.beta.assistants.create(
    name="Atendente EcoMart",
    instructions=f"""
        Você é um chatbot de atendimento a clientes de um e-commerce. 
        Você não deve responder perguntas que não sejam dados do ecommerce informado!
        Além disso, adote a persona abaixo para responder ao cliente.
        
        ## Contexto
        {contexto}
        
        ## Persona
        
        {personas["neutro"]}
    """,
    model=modelo,
)

print(assistente.id)

# Passo 1 - Crio uma Thread com uma pergunta incompleta
thread = cliente.beta.threads.create(
    messages=[{"role": "user", "content": "Liste os produtos"}]
)

# Passo 2 - adiciono uma segunda pergunta a mesma thread
cliente.beta.threads.messages.create(
    thread_id=thread.id, role="user", content=" da categoria moda sustentável"
)

# Passo 3 - mando rodar a Thread passando o ID da thread e o ID do assistente
run = cliente.beta.threads.runs.create(thread_id=thread.id, assistant_id=assistente.id)

# Passo 4 - Fico verificando se a thread está completa, se estiver eu recebo o resultado
while run.status != "completed":
    run = cliente.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)

# Passo 5 - Recebo uma lista de resultados da Thread (resposta da OpenAI)
historico = cliente.beta.threads.messages.list(thread_id=thread.id).data

# Passo 6 - Varro a lista em ordem reversa (reversed) e imprimo com formatação melhor no terminal
for mensagem in reversed(historico):
    print(f"role: {mensagem.role}\nConteúdo: {mensagem.content[0].text.value}")
