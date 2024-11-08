from flask import Flask, render_template, request, Response
from openai import OpenAI
from dotenv import load_dotenv
import os
from time import sleep
from helpers import *  # vai importar o helper the ler e gravar arquivo
from selecionar_persona import *
from selecionar_documento import *

load_dotenv()

cliente = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
modelo = "gpt-4o-mini"  # alterei para usar o modelo mais básico do ChatGPT

app = Flask(__name__)
app.secret_key = "alura"

# contexto = carrega("dados/ecomart.txt")  # aqui tem as informações sobre o ecommerce


def bot(prompt):
    maximo_tentativas = 1
    repeticao = 0
    # a ideia do helper é entender o humor do meu usuário, e adaptar o chatBot pra responder de maneira adequada
    # se o usuário estiver bravo, ele vai focar em resolver, se estiver feliz ele será mais ameno. Leia o texto pra entender
    personalidade = personas[selecionar_persona(prompt)]
    contexto = selecionar_contexto(prompt)
    documento_selecionado = selecionar_documento(contexto)

    while True:
        try:
            # note que eu instruo o chatGPT a ignorar perguntas que não sejam relativas ao e-commerce
            # note que eu informei o contexto que é o arquivo de texto ecomart.txt que contém tudo sobre o ecommnerce
            prompt_do_sistema = f"""
            Você é um chatbot de atendimento a clientes de um e-commerce. 
            Você não deve responder perguntas que não sejam dados do ecommerce informado!
            Você deve gerar respostas utilizando o contexto abaixo.
            Você deve adotar a persona abaixo.
            
            # Contexto
            {documento_selecionado}
            
            # Persona
            {personalidade}
            """
            response = cliente.chat.completions.create(
                messages=[
                    {"role": "system", "content": prompt_do_sistema},
                    {"role": "user", "content": prompt},
                ],
                temperature=1,
                max_tokens=300,  # evita que a resposta seja enorme
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                model=modelo,
            )
            return response
        except Exception as erro:
            repeticao += 1
            if repeticao >= maximo_tentativas:
                return "Erro no GPT: %s" % erro
            print("Erro de comunicação com OpenAI:", erro)
            sleep(1)


@app.route(
    "/chat", methods=["POST"]
)  # esse método é chamado pelo JS index.js para interagir
def chat():
    prompt = request.json["msg"]
    resposta = bot(prompt)  # envio a pergunta para o chat gpt
    texto_resposta = resposta.choices[0].message.content
    return texto_resposta  # retorna a resposta pro JS que irá renderizar


@app.route("/")  # na minha rota padrão eu carrego o index.html
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
