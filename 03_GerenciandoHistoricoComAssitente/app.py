from flask import Flask, render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *  # vai importar o helper the ler e gravar arquivo
from selecionar_persona import *
from selecionar_documento import *
from assistente_ecomart import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4o-mini"  # alterei para usar o modelo mais básico do ChatGPT

app = Flask(__name__)
app.secret_key = "alura"

assistente = (
    criar_assistente()
)  # abro essa classe já criando um assistente e uma thread
thread = criar_thread()


def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0

    while True:
        try:
            # Passo 1 - envio a mensagem do usuário para o meu cliente com a thread criada
            cliente.beta.threads.messages.create(
                thread_id=thread.id, role="user", content=prompt
            )

            # Passo 2 - Mando rodar a thread com o assistente ID
            run = cliente.beta.threads.runs.create(
                thread_id=thread.id, assistant_id=assistente.id
            )

            # Passo 3 - aguardo a thread ser completada
            while run.status != "completed":
                run = cliente.beta.threads.runs.retrieve(
                    thread_id=thread.id, run_id=run.id
                )

            # Passo 4 - Converto o histórico em lista (boxing)
            historico = list(
                cliente.beta.threads.messages.list(thread_id=thread.id).data
            )
            resposta = historico[0]
            return resposta  # retorno a resposta

        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro no GPT: %s" % erro
            print("Erro de comunicação com OpenAI", erro)
            sleep(1)


@app.route(
    "/chat", methods=["POST"]
)  # esse método é chamado pelo JS index.js para interagir
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)  # envio a pergunta para o chat gpt
    texto_resposta = resposta.content[
        0
    ].text.value  # aqui precisou MUDAR pra pegar no formato que a thread retorna
    return texto_resposta  # retorna a resposta pro JS que irá renderizar


@app.route("/")  # na minha rota padrão eu carrego o index.html
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
