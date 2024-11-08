import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from helpers import load
from tools import tools

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
model = "gpt-4-1106-preview"

context = load("data/ecomart.txt")


# irá criar uma thread com o ID do Vector Store (onde estão os arquivos de texto)
def create_thread(vector_store):
    return client.beta.threads.create(
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}}
    )


# irá criar o Vector store com os 3 arquivos de texto com dados da ecomart
def create_vector_store():
    vector_store = client.beta.vector_stores.create(name="Ecomart Vector Store")

    file_paths = [
        "data/ecomart_data.txt",
        "data/ecomart_politics.txt",
        "data/ecomart_products.txt",
    ]
    file_streams = [open(path, "rb") for path in file_paths]
    # upload dos arquivos
    client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    return vector_store


# irá criar o assistente também usando a vector store id para que ele use aqueles arquivos
def create_assistant(vector_store):
    assistant = client.beta.assistants.create(
        name="Ecomart Assistant",
        instructions=f"""
            Você é um chatbot de atendimento a clientes de um e-commerce. 
            Você não deve responder perguntas que não sejam dados do ecommerce informado!
            Além disso, acesse os arquivos associados a você e a thread para responder as perguntas.
        """,
        model=model,
        tools=tools,  # irá criar a function que faz validação de cupons
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )
    return assistant


# recupera o assistente ID e a vector store ID para criar usando os dados que estão no json
def get_json():
    filename = "assistants.json"

    # se o arquivo assistants.json não existir, apenas ai ele irá chamar o criar assistente! legal...
    if not os.path.exists(filename):
        vector_store = create_vector_store()
        thread = create_thread(vector_store)
        assistant = create_assistant(vector_store)

        data = {
            "assistant_id": assistant.id,
            "vector_store_id": vector_store.id,
            "thread_id": thread.id,
        }

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        print('Arquivo "assistentes.json" criado com sucesso.')

    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print('Arquivo "assistentes.json" não encontrado.')
